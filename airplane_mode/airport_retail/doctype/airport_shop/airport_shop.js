// Copyright (c) 2026, Goprime Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
	refresh(frm) {
        frm.set_query("shop_type", {
            filters: {
                "enabled": 1
            }
        })

        frm.add_custom_button("Show Previous Tenants", () => {
            
            frappe.call({
                method: "show_previous_tenants",
                doc: frm.doc
            }).then(res => {

                frappe.msgprint(res.message)
            })
        }, "Actions")
    },
});
