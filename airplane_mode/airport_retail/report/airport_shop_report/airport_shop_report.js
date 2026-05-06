// Copyright (c) 2026, Goprime Systems and contributors
// For license information, please see license.txt

frappe.query_reports["Airport Shop Report"] = {
	"filters": [
		{
			fieldname: "airport",
			fieldtype: "Link",
			options: "Airport",
			label: "Airport"
		}
	]
};
