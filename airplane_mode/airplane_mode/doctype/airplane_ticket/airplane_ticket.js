// Copyright (c) 2026, Goprime Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		frm.trigger("set_intro");
		frm.trigger("add_actions");
	},

	set_intro(frm) {
		const statusMessages = {
			"Booked": [__("Ticket is booked. Check in to proceed."), "blue"],
			"Checked-In": [__("Passenger is checked in."), "green"],
			"Boarded": [__("Passenger has boarded."), "purple"],
		};
		const [msg, color] = statusMessages[frm.doc.status] || ["", ""];
		frm.set_intro(msg, color);
	},

	add_actions(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Assign Seat"), () => {
				const d = new frappe.ui.Dialog({
					title: __("Select Seat"),
					fields: [
						{
							fieldname: "seat_number",
							fieldtype: "Data",
							label: __("Seat Number"),
						},
					],
					primary_action_label: __("Assign"),
					primary_action(values) {
						if (!values.seat_number) {
							frappe.throw(__("Please enter a seat number."));
						}
						// Confirm before assigning — seat changes are significant
						frappe.confirm(
							__("Assign seat {0} to this passenger?", [values.seat_number]),
							() => {
								frm.set_value("seat", values.seat_number);
								d.hide();
								// Always show a success message after action completes
								frappe.show_alert({
									message: __("Seat {0} assigned.", [values.seat_number]),
									indicator: "green",
								});
							}
						);
					},
				});
				d.show();
			}, __("Actions"));
		}

		if (frm.doc.flight && !frm.is_new()) {
			const flightLink = frappe.utils.get_link_to_form("Airplane Flight", frm.doc.flight);
			frm.add_custom_button(__("View Flight"), () => {
				window.open(flightLink, "_blank");
			});
		}
	},

	status(frm) {
		frm.trigger("set_intro");
	},
});
