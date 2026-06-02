# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirportShop(WebsiteGenerator):
	
	@frappe.whitelist()
	def show_previous_tenants(self):
		tenants = frappe.db.sql('''
			select 
				tenant 
			from
				`tabAirport Shop Rental Contract`
			where 
				shop = %s 			
		''', self.name)

		if not tenants:
			return "No Tenants found"
		return f"<ul><li>{'</li><li>'.join([t[0] for t in tenants])}</li></ul>"
