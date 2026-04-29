# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from airplane_mode.airport_retail.util import get_rent_due


class AirportRentPayment(Document):
	@frappe.whitelist()
	def get_rent_details(self):
		return get_rent_due(self.lease)