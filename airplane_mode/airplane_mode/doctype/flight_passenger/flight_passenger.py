# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	# full_name is a virtual field — its value is computed from the Options
	# f-string expression in the DocType definition; no controller logic needed.
	pass
