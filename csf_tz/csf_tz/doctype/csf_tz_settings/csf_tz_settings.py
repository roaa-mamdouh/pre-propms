# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CSFTZSettings(Document):
	def validate(self):
		if self.enable_fixed_working_days_per_month and (self.working_days_per_month < 1 or self.working_days_per_month > 30):
			frappe.throw("Working days per month must be between 1 and 30")
