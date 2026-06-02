# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import format_duration, formatdate, format_time


def get_context(context):
	context.title = "All Flights — Airplane Mode"
	context.no_cache = 1

	fd = frappe.form_dict
	filters = {}

	if fd.get("from"):
		filters["source_airport_code"] = ["like", f"%{fd['from'].upper()}%"]
	if fd.get("to"):
		filters["destination_airport_code"] = ["like", f"%{fd['to'].upper()}%"]
	if fd.get("date"):
		filters["date_of_departure"] = fd["date"]
	if fd.get("status"):
		filters["status"] = fd["status"]
	else:
		filters["status"] = ["!=", "Cancelled"]

	raw = frappe.get_all(
		"Airplane Flight",
		filters=filters,
		fields=[
			"name", "airplane", "status",
			"source_airport", "source_airport_code",
			"destination_airport", "destination_airport_code",
			"date_of_departure", "time_of_departure", "duration",
		],
		order_by="date_of_departure asc, time_of_departure asc",
		limit=100,
	)

	# Enrich each row with display values and airline name
	flights = []
	for f in raw:
		airline = ""
		if f.airplane:
			airline = frappe.db.get_value("Airplane", f.airplane, "airline") or ""

		flights.append(frappe._dict({
			**f,
			"airline": airline,
			"date_display": formatdate(f.date_of_departure, "d MMM yyyy") if f.date_of_departure else "—",
			"time_display": str(f.time_of_departure)[:5] if f.time_of_departure else "—",
			"duration_display": format_duration(f.duration) if f.duration else "",
		}))

	context.flights = flights
