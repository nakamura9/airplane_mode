// Copyright (c) 2026, Goprime Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
        frm.add_custom_button(__("Assign Seat"), () => {
            const d = new frappe.ui.Dialog({
                "title": "Select Seat",
                "fields": [
                    {
                        fieldname: "seat_number",
                        fieldtype: "Data",
                        label: "Seat Number"
                    }
                ],
                "primary_action": function(values) {
                    if(!values.seat_number)
                        frappe.throw("Missing seat number!")
                    frm.set_value("seat", values.seat_number)
                    d.hide()
                }
            })
            d.show()
        }, __("Actions"))
	},
});
