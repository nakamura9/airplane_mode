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

        if(frm.doc.__islocal) {
            frappe.db.get_doc("Airport Retail Settings", "Airport Retail Settings")
                .then(res => {
                    if(res.default_rent_for_shops)
                        frm.set_value("monthly_rent", res.default_rent_for_shops);
                })
        }
        
	},
});
