// Copyright (c) 2026, Goprime Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Rent Payment", {
	refresh(frm) {

	},
    lease: function(frm) {
        frappe.call({
            doc:frm.doc,
            method: "get_rent_details",
            args: {
                lease: frm.doc.lease
            }
        }).then(res => {
            frm.set_value("amount_due", res.message)
        })
    }
});
