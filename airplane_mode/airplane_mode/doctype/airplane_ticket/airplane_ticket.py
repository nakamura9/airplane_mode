# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
import random
import string


@frappe.whitelist()
def get_tickets_for_airline(airline):
	"""Demo: dot-notation join — filter Airplane Ticket rows by a grandparent field.

	frappe.get_all supports "child_table.fieldname" notation for automatic joins,
	so there is no need for raw SQL.

	  airline (Airline)
	    └─ airplane (Airplane)
	         └─ flight (Airplane Flight)
	              └─ ticket (Airplane Ticket)  ← what we're querying

	The filter "flight.airplane.airline" traverses two levels of Link fields.
	"""
	frappe.errprint(f"[airplane_ticket] get_tickets_for_airline called with airline={airline!r}")

	tickets = frappe.get_all(
		"Airplane Ticket",
		filters={"flight.airplane.airline": airline},
		fields=["name", "passenger", "status", "total_amount", "flight"],
	)

	frappe.errprint(f"[airplane_ticket] found {len(tickets)} tickets for {airline!r}")
	return tickets

class AirplaneTicket(Document):
	def before_save(self):
		self.set_seat_number()
		self.validate_ticket_count()


	def validate_ticket_count(self):
		plane_capacity = frappe.db.get_value("Airplane Flight", self.flight, "airplane.capacity")
		ticket_count = len(frappe.get_all("Airplane Ticket", filters={
			"flight": self.flight
		}))

		if ticket_count >= plane_capacity:
			frappe.throw("The number of issued tickets meet or exceed the airplane capacity.")

	def set_seat_number(self):
		letter_choices = "ABCDE"
		if not self.seat:
			self.seat = f"{random.randint(0,9)}"
			self.seat += f"{random.randint(0,9)}"
			self.seat += random.choice(letter_choices)
			self.seat += random.choice(letter_choices)

	def validate(self):
		unique_add_ons = set()
		addons_to_remove = []
		self.total_amount = self.flight_price
		for addon in self.add_ons:
			if addon.item in unique_add_ons:
				addons_to_remove.append(addon)
				continue
			unique_add_ons.add(addon.item)
			self.total_amount += flt(addon.amount)

		for addon in addons_to_remove:
			self.remove(addon)


			

	def before_submit(self):
		if not self.status == "Boarded":
			frappe.throw(
				"Cannot submit a ticket in the {} status".format(self.status),
				title="Invalid Status"
			)

	def on_submit(self):
		self.status = "Completed"