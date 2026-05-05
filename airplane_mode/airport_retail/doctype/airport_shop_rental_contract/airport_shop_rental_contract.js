// Copyright (c) 2026, Goprime Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop Rental Contract", {
	refresh(frm) {
        if(frm.doc.docstatus === 1) {
            frappe.add_custom_button("Pay Rent", () => {
            frappe.new_doc("Airport Rent Payment", {
                    "lease": frm.doc.name,
                    "date": frappe.utils.nowdate()
                })
            }, "Actions")
        }
	},
});
