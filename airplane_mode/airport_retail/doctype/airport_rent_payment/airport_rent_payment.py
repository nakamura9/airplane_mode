# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from airplane_mode.airport_retail.util import get_rent_due


class AirportRentPayment(Document):
	@frappe.whitelist()
	def get_rent_details(self):
		return get_rent_due(self.lease)

	def on_submit(self):
		self._update_schedule_amount_paid(delta=self.amount_paid)

	def on_cancel(self):
		self._update_schedule_amount_paid(delta=-self.amount_paid)

	def _update_schedule_amount_paid(self, delta):
		payment_date = frappe.utils.getdate(self.date)
		key = (payment_date.year, payment_date.month)

		rows = frappe.get_all(
			"Rental Payment Schedule Item",
			filters={"parent": self.lease},
			fields=["name", "date", "amount_paid"],
		)

		for row in rows:
			row_date = frappe.utils.getdate(row.date)
			if (row_date.year, row_date.month) == key:
				frappe.db.set_value(
					"Rental Payment Schedule Item",
					row.name,
					"amount_paid",
					max(0, (row.amount_paid or 0) + delta),
				)