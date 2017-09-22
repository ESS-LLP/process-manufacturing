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

def add_item_in_table(self, table_value, table_name):
	clear_table(self, table_name)

	for item in table_value:
		po_item = self.append(table_name, {})
		po_item.item = item.item
		po_item.item_name = item.item_name

def clear_table(self, table_name):
	self.set(table_name, [])
