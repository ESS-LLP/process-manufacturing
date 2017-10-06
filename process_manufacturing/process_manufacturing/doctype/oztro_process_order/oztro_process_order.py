# -*- coding: utf-8 -*-
# Copyright (c) 2017, earthians and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime
from frappe import _

class OztroProcessOrder(Document):
	def get_process_details(self):
		#	Set costing_method
		self.costing_method = frappe.db.get_value("Oztro Process", self.process_name, "costing_method")
		#	Set Child Tables
		process = frappe.get_doc("Oztro Process", self.process_name)
		if process:
			if process.materials:
				add_item_in_table(self, process.materials, "materials")
			if process.finished_products:
				add_item_in_table(self, process.finished_products, "finished_products")
			if process.scrap:
				add_item_in_table(self, process.scrap, "scrap")

	def start_finish_processing(self, status):
		return self.make_stock_entry(status)

	def set_se_items_start(self, se):
		for item in self.materials:
			src_wh = frappe.db.get_value("Item", item.item, "default_warehouse")
			se = self.set_se_items(se, item, src_wh, se.from_warehouse, "Start", None, None)

		return se

	def set_se_items_finish(self, se):
		se_materials = frappe.get_doc("Stock Entry",{"oztro_process_order": self.name, "docstatus": '1'})
		if se_materials:
			se.items = se_materials.items
			for item in se.items:
				item.s_warehouse = se.from_warehouse
				item.t_warehouse = None
		else:
			for item in self.materials:
				se = self.set_se_items(se, item, se.from_warehouse, None, "Finish", None, None)

		qty_of_total_production = 0
		total_sale_value = 0
		for item in self.finished_products:
			qty_of_total_production = float(qty_of_total_production) + item.quantity
			sale_value_of_pdt = frappe.db.get_value("Item Price", {"item_code":item.item}, "price_list_rate")
			if sale_value_of_pdt:
				total_sale_value += float(sale_value_of_pdt) * item.quantity
		for item in self.scrap:
			qty_of_total_production = float(qty_of_total_production + item.quantity)
			sale_value_of_pdt = frappe.db.get_value("Item Price", {"item_code":item.item}, "price_list_rate")
			if sale_value_of_pdt:
				total_sale_value += float(sale_value_of_pdt) * item.quantity

		for item in self.finished_products:
			se = self.set_se_items(se, item, None, se.to_warehouse, "Finish", qty_of_total_production, total_sale_value)

		for item in self.scrap:
			se = self.set_se_items(se, item, None, self.scrap_warehouse, "Finish", qty_of_total_production, total_sale_value)

		return se

	def set_se_items(self, se, item, s_wh, t_wh, status, qty_of_total_production, total_sale_value):
		expense_account, cost_center = frappe.db.get_values("Company", self.company, \
				["default_expense_account", "cost_center"])[0]
		item_name, stock_uom, description, item_expense_account, item_cost_center = frappe.db.get_values("Item", item.item, \
		["item_name", "stock_uom", "description", "expense_account", "buying_cost_center"])[0]

		if not expense_account and not item_expense_account:
			frappe.throw(_("Please update default Default Cost of Goods Sold Account for company {0}").format(self.company))

		if not cost_center and not item_cost_center:
			frappe.throw(_("Please update default Cost Center for company {0}").format(self.company))

		if item.quantity > 0:
			sale_value_of_pdt = frappe.db.get_value("Item Price", {"item_code":item.item}, "price_list_rate")
			se_item = se.append("items")
			se_item.item_code = item.item
			se_item.qty = item.quantity
			se_item.s_warehouse = s_wh
			se_item.t_warehouse = t_wh
			se_item.item_name = item_name
			se_item.description = description
			se_item.uom = stock_uom
			se_item.stock_uom = stock_uom

			se_item.expense_account = item_expense_account or expense_account
			se_item.cost_center = item_cost_center or cost_center

			# in stock uom
			se_item.transfer_qty = item.quantity
			se_item.conversion_factor = 1.00

			if status == "Start":
			  item_details = se.run_method( "get_item_details",args = (frappe._dict(
			    {"item_code": item.item, "company": self.company, "uom": "Nos", 's_warehouse': s_wh})), for_update=True)

			  for f in ("uom", "stock_uom", "description", "item_name", "expense_account",
			    "cost_center", "conversion_factor"):
			      if f in ["stock_uom", "conversion_factor"] or not item.get(f):
			        se_item.set(f, item_details.get(f))

			if status == "Finish":

				se_materials = frappe.get_doc("Stock Entry",{"oztro_process_order": self.name, "docstatus": '1'})
				if se_materials:
					total_production_cost = se_materials.total_incoming_value
				se_item.basic_rate = self.basic_rate(item.quantity, qty_of_total_production, sale_value_of_pdt, total_sale_value, total_production_cost)

		if se.items:
			return se

	def basic_rate(self, qty_of_pdt, total_qty, sale_value_of_pdt, total_sale_value, total_production_cost):
		if total_production_cost > 0 and total_sale_value > 0 and qty_of_pdt > 0 and total_qty > 0:
			if self.costing_method == "Relative Sales Value":
				basic_rate = (float(sale_value_of_pdt) * float(total_production_cost)) / float(total_sale_value)
			if self.costing_method == "Physical measurement":
				basic_rate = float(total_production_cost) / float(total_qty)

			return basic_rate

	def make_stock_entry(self, status):
		if self.wip_warehouse:
			wip_warehouse = self.wip_warehouse
		else:
			wip_warehouse = frappe.db.get_single_value("Manufacturing Settings", "default_wip_warehouse")
		if self.fg_warehouse:
			fg_warehouse = self.fg_warehouse
		else:
			fg_warehouse = frappe.db.get_single_value("Manufacturing Settings", "default_fg_warehouse")

		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.oztro_process_order = self.name
		stock_entry.from_warehouse = wip_warehouse
		stock_entry.to_warehouse = fg_warehouse
		if status == "Start":
			stock_entry.purpose = "Material Transfer for Manufacture"
			stock_entry = self.set_se_items_start(stock_entry)
		if status == "Finish":
			stock_entry.purpose = "Manufacture"
			stock_entry = self.set_se_items_finish(stock_entry)

		return stock_entry.as_dict()

def add_item_in_table(self, table_value, table_name):
	clear_table(self, table_name)

	for item in table_value:
		po_item = self.append(table_name, {})
		po_item.item = item.item
		po_item.item_name = item.item_name

def clear_table(self, table_name):
	self.set(table_name, [])

@frappe.whitelist()
def submit_se(doc, method):
	if doc.oztro_process_order:
		oztro_po = frappe.get_doc("Oztro Process Order", doc.oztro_process_order)
		if oztro_po.status == "Open":
			oztro_po.status = "Start"
			oztro_po.start_dt = get_datetime()
		elif oztro_po.status == "Start":
			oztro_po.status = "Finish"
		oztro_po.save()
