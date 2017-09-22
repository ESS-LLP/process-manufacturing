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
		
