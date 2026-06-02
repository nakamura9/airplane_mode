# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

import frappe


def get_context(context):
	context.title = "Airplane Mode — Book Flights"
	context.no_cache = 1

	context.total_flights = frappe.db.count("Airplane Flight", {"status": "Scheduled"})
	context.total_airlines = frappe.db.count("Airline")
	context.total_airports = frappe.db.count("Airport")
