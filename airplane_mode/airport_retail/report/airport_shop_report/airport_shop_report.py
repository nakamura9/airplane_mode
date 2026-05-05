# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

import frappe

def get_data(filters):
	airports = frappe.get_all("Airport", pluck="name")
	if filters:
		airports = [filters.airport]
	
	data = []
	for airport_name in airports:
		row = {"airport": airport_name}
		shops = frappe.get_all("Airport Shop", filters={
			"airport": airport_name
		}, fields=["current_lease", "name"])
		row["shop_count"] = len(shops)
		row["available_shop_count"] = len([s for s in shops if not s.get("current_lease")])
		row["leased_shop_count"] = len([s for s in shops if s.get("current_lease")])

		data.append(row)

	return data


def get_columns():
	return [
		{
			"fieldname": "airport",
			"fieldtype": "Link",
			"label": "Airport",
			"options": "Airport"
		},
		{
			"fieldname": "shop_count",
			"fieldtype": "Int",
			"label": "No. of Shops"
		},
		{
			"fieldname": "available_shop_count",
			"fieldtype": "Int",
			"label": "Available Shops"
		},
		{
			"fieldname": "leased_shop_count",
			"fieldtype": "Int",
			"label": "Leased out Shops"
		},
	]


def execute(filters=None):
	data = get_data(filters)
	columns = get_columns()
	return columns, data
