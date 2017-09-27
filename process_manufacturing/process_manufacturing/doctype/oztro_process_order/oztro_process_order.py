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

	def start_finish_processing(self, status):
		self.status = status
		self.save()
		return self.make_stock_entry(status)

	def set_se_items_start(self, se):
		for item in self.materials:
			se = self.set_se_items(se, item, frappe.db.get_value("Item", item.item, "default_warehouse"), se.from_warehouse)
		return se

	def set_se_items_finish(self, se):
		for item in self.materials:
			se = self.set_se_items(se, item, se.from_warehouse, None)

		for item in self.finished_products:
			se = self.set_se_items(se, item, None, se.to_warehouse)

		for item in self.scrap:
			se = self.set_se_items(se, item, None, self.scrap_warehouse)

		return se

	def set_se_items(self, se, item, s_wh, t_wh):
		if item.quantity > 0:
			se_item = se.append("items")
			se_item.item_code = item.item
			se_item.qty = item.quantity
			se_item.s_warehouse = s_wh
			se_item.t_warehouse = t_wh
		return se

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
		stock_entry.purpose = "Manufacture"

		stock_entry.from_warehouse = wip_warehouse
		stock_entry.to_warehouse = fg_warehouse
		if status == "Start":
			self.set_se_items_start(stock_entry)
		if status == "Finish":
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
