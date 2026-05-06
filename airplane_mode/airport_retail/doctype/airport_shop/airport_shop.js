// Copyright (c) 2026, Goprime Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
	refresh(frm) {
        frm.set_query("shop_type", {
            filters: {
                "enabled": 1
            }
        })
    },
});
