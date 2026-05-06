# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

def update_ticket_gates(flight, gate):
	tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight}, pluck="name")
	for ticket_name in tickets:
		frappe.db.set_value("Airplane Ticket", ticket_name, gate)


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.status = "Completed"

	def on_update(self):
		previous = self.get_doc_before_save()
		if previous.source_airport_gate != self.source_airport_gate:
			frappe.enqueue(
				method=update_ticket_gates,
				is_async=True,
				flight=self.name,
				gate=self.source_airport_gate
			)
