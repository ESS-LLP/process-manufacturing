# -*- coding: utf-8 -*-
# Copyright (c) 2017, earthians and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

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

	def start_processing(self):
		self.status = "Start"
		self.save()
		return self.make_stock_entry_start()

	def finish_processing(self):
		self.status = "Finish"
		self.save()
		return self.make_stock_entry_finish()

	def make_stock_entry_start(self):
		if self.wip_warehouse:
			wip_warehouse = self.wip_warehouse
		else:
			wip_warehouse = frappe.db.get_single_value("Manufacturing Settings", "default_wip_warehouse")
		if self.fg_warehouse:
			fg_warehouse = self.fg_warehouse
		else:
			fg_warehouse = frappe.db.get_single_value("Manufacturing Settings", "default_fg_warehouse")

		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.purpose = "Manufacture"

		stock_entry.from_warehouse = wip_warehouse
		stock_entry.to_warehouse = fg_warehouse
		stock_entry = self.set_se_items_start(stock_entry)
		return stock_entry.as_dict()

	def set_se_items_start(self, se):
		for item in self.materials:
			if item.quantity > 0:
				se_item = se.append("items")
				se_item.item_code = item.item
				se_item.qty = item.quantity
				se_item.s_warehouse = frappe.db.get_value("Item", item.item, "default_warehouse")
				se_item.t_warehouse = se.from_warehouse

		return se

	def make_stock_entry_finish(self):
		if self.wip_warehouse:
			wip_warehouse = self.wip_warehouse
		else:
			wip_warehouse = frappe.db.get_single_value("Manufacturing Settings", "default_wip_warehouse")
		if self.fg_warehouse:
			fg_warehouse = self.fg_warehouse
		else:
			fg_warehouse = frappe.db.get_single_value("Manufacturing Settings", "default_fg_warehouse")

		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.purpose = "Manufacture"

		stock_entry.from_warehouse = wip_warehouse
		stock_entry.to_warehouse = fg_warehouse
		stock_entry = self.set_se_items_finish(stock_entry)
		return stock_entry.as_dict()

	def set_se_items_finish(self, se):
		for item in self.materials:
			if item.quantity > 0:
				se_item = se.append("items")
				se_item.item_code = item.item
				se_item.qty = item.quantity
				se_item.s_warehouse = se.from_warehouse

		for item in self.finished_products:
			if item.quantity > 0:
				se_item = se.append("items")
				se_item.item_code = item.item
				se_item.qty = item.quantity
				se_item.t_warehouse = se.to_warehouse

		for item in self.scrap:
			if item.quantity > 0:
				se_item = se.append("items")
				se_item.item_code = item.item
				se_item.qty = item.quantity
				se_item.t_warehouse = self.scrap_warehouse

		return se

	def make_stock_entry(self, purpose, material_pdt, status):
		if self.wip_warehouse:
			wip_warehouse = self.wip_warehouse
		else:
			wip_warehouse = frappe.db.get_single_value("Manufacturing Settings", "default_wip_warehouse")
		if self.fg_warehouse:
			fg_warehouse = self.fg_warehouse
		else:
			fg_warehouse = frappe.db.get_single_value("Manufacturing Settings", "default_fg_warehouse")

		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.purpose = purpose

		stock_entry.from_warehouse = wip_warehouse
		stock_entry.to_warehouse = fg_warehouse
		stock_entry = set_se_items(stock_entry, material_pdt, status, wip_warehouse, fg_warehouse)
		return stock_entry.as_dict()

def set_se_items(se, material_pdt, s_wh = None, t_wh = None):
	for item in material_pdt:
		se_item = se.append("items")
		se_item.item_code = item.item
		se_item.qty = item.quantity
		if status == "Start":
			se_item.s_warehouse = frappe.db.get_value("Item", item.item, "default_warehouse")
			se_item.t_warehouse = se.from_warehouse
		if status == "Fiinish":
			se_item.s_warehouse = s_wh
			se_item.t_warehouse = t_wh

	return se

def add_item_in_table(self, table_value, table_name):
	clear_table(self, table_name)

	for item in table_value:
		po_item = self.append(table_name, {})
		po_item.item = item.item
		po_item.item_name = item.item_name

def clear_table(self, table_name):
	self.set(table_name, [])
