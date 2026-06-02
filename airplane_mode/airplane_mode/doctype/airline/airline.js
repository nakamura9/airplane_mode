// Copyright (c) 2026, Goprime Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	// on_load runs once — use refresh so the link re-renders on every reload
	refresh(frm) {
		if (frm.doc.website) {
			frm.add_web_link(frm.doc.website, "Visit Website");
		}
	},
});
