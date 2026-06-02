// Copyright (c) 2026, Goprime Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	refresh(frm) {
		frm.trigger("set_intro");
		frm.trigger("add_actions");
	},

	// Reusable logic defined as a named trigger — call frm.trigger("set_intro")
	// from any event instead of duplicating the same conditional block.
	set_intro(frm) {
		if (frm.doc.status === "Cancelled") {
			frm.set_intro(__("This flight has been cancelled."), "red");
		} else if (frm.doc.status === "Completed") {
			frm.set_intro(__("This flight has been completed."), "green");
		} else if (!frm.doc.source_airport_gate) {
			frm.set_intro(__("Gate not yet assigned — assign one before departure."), "orange");
		} else {
			frm.set_intro("");
		}
	},

	add_actions(frm) {
		if (frm.doc.docstatus === 0 && frm.doc.status !== "Cancelled") {
			frm.add_custom_button(__("Cancel Flight"), () => {
				// Always confirm destructive/significant actions
				frappe.confirm(
					__("Are you sure you want to cancel this flight? All linked tickets will be affected."),
					() => {
						frappe.call({
							method: "frappe.client.set_value",
							args: {
								doctype: "Airplane Flight",
								name: frm.doc.name,
								fieldname: "status",
								value: "Cancelled",
							},
							callback() {
								frm.reload_doc();
								// Always show a success message after an action completes
								frappe.show_alert({
									message: __("Flight {0} cancelled.", [frm.doc.name]),
									indicator: "red",
								});
							},
						});
					}
				);
			}, __("Actions"));
		}

		if (frm.doc.docstatus === 0 && frm.doc.status === "Scheduled") {
			frm.add_custom_button(__("Run Pre-flight Checklist"), () => {
				frm.trigger("run_checklist");
			}, __("Actions"));
		}

		if (!frm.is_new()) {
			frm.add_custom_button(__("View Tickets"), () => {
				// frappe.utils.get_link_to_form for programmatic navigation links
				const link = frappe.utils.get_link_to_form(
					"Airplane Ticket",
					null,
					`?flight=${encodeURIComponent(frm.doc.name)}`
				);
				window.open(link, "_blank");
			});
		}
	},

	run_checklist(frm) {
		// Show a progress dialog while the background job runs
		const dialog = new frappe.ui.Dialog({
			title: __("Running Pre-flight Checklist"),
			fields: [
				{
					fieldtype: "HTML",
					fieldname: "progress_html",
					options: `<div id="checklist-progress">
						<div class="progress" style="height:20px;">
							<div id="checklist-bar"
								class="progress-bar progress-bar-striped progress-bar-animated"
								style="width:0%">0%</div>
						</div>
						<p id="checklist-step" class="mt-2 text-muted"></p>
					</div>`,
				},
			],
		});
		dialog.show();

		// frappe.realtime.on — client subscription scoped to this doctype+name
		frappe.realtime.on("flight_checklist_progress", (data) => {
			const bar = document.getElementById("checklist-bar");
			const step = document.getElementById("checklist-step");
			if (bar) {
				bar.style.width = data.progress + "%";
				bar.textContent = data.progress + "%";
			}
			if (step) step.textContent = data.step;

			if (data.completed) {
				frappe.realtime.off("flight_checklist_progress");
				dialog.set_title(__("Checklist Complete"));
				frappe.show_alert({
					message: __("Pre-flight checklist passed."),
					indicator: "green",
				});
			}
		});

		frappe.call({
			method: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.run_flight_checklist",
			args: { flight_name: frm.doc.name },
			// frappe.enqueue is called server-side — the response returns quickly
			callback(r) {
				if (r.exc) {
					dialog.hide();
					frappe.realtime.off("flight_checklist_progress");
				}
			},
		});
	},

	status(frm) {
		// Re-run intro whenever status changes so colour stays in sync
		frm.trigger("set_intro");
	},

	source_airport_gate(frm) {
		frm.trigger("set_intro");
	},
});

// Child-table hooks — fired when a crew row is added or removed
frappe.ui.form.on("Airplane Flight Crew Item", {
	table_jtxs_add(frm) {
		frappe.show_alert({
			message: __("Crew member row added — remember to save."),
			indicator: "blue",
		});
	},

	table_jtxs_remove(frm) {
		frappe.show_alert({
			message: __("Crew member removed."),
			indicator: "orange",
		});
	},
});
