# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt
import frappe
from frappe.query_builder import DocType

def get_data(filters):
	airline_names = frappe.get_all("Airline", pluck="name")
	airline_revenue_map = {i: 0 for i in airline_names} 
	AirplaneTicket = DocType("Airplane Ticket")
	AirplaneFlight = DocType("Airplane Flight")
	Airplane = DocType("Airplane")
	tickets = (frappe.qb
		.from_(AirplaneTicket)
		.join(AirplaneFlight)
		.on(AirplaneFlight.name == AirplaneTicket.flight)
		.join(Airplane)
		.on(Airplane.name == AirplaneFlight.airplane)
		.where(AirplaneTicket.docstatus == 1)
		.select(AirplaneTicket.total_amount, Airplane.airline)
	)
	for ticket in tickets.run(as_dict=True):
		airline_revenue_map.setdefault(ticket.airline, 0)
		airline_revenue_map[ticket.airline] += ticket.total_amount

	return [frappe._dict({
		"airline": al,
		"revenue": airline_revenue_map.get(al, 0)
	}) for al in airline_revenue_map]


def get_columns():
	return [
		{
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline",
			"label": "Airline"
		},
		{
			"fieldname": "revenue",
			"fieldtype": "Currency",
			"options": "USD",
			"label": "Revenue"
		}
	]


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = {
		"data": {
			"labels": [i.airline for i in data],
			"datasets":[ 
				{	
					"name": "Revenue",
					"values": [i.revenue for i in data]
				}
			]
		},
		"type": "donut"
	}
	total = sum(i.revenue for i in data)
	summary = [
		{
            "value": total,
            "label": "Total Revenue",
            "datatype": "Currency",
            "currency": "USD",
			"indicator": "Orange"
        },
	]

	return columns, data, "", chart, summary
