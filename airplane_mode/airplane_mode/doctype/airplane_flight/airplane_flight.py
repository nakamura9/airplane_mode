# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


def _run_checklist_steps(flight_name):
	"""Background worker — publishes realtime progress for each checklist step.

	Not whitelisted; called via frappe.enqueue from run_flight_checklist.
	"""
	import time

	steps = [
		"Verifying crew manifest",
		"Confirming gate assignment",
		"Checking fuel load",
		"Clearance from tower",
		"Checklist complete",
	]
	total = len(steps)
	for i, step in enumerate(steps, start=1):
		time.sleep(1)
		# frappe.publish_realtime — server push scoped to this document
		frappe.publish_realtime(
			"flight_checklist_progress",
			{
				"step": step,
				"progress": round((i / total) * 100),
				"completed": i == total,
			},
			doctype="Airplane Flight",
			docname=flight_name,
		)


@frappe.whitelist()
def run_flight_checklist(flight_name):
	"""Demo: enqueue a background job that pushes realtime progress events.

	The call returns immediately; the worker runs in the background and
	pushes updates via WebSockets.  The client subscribes with:
	  frappe.realtime.on("flight_checklist_progress", callback)
	"""
	frappe.enqueue(
		method=_run_checklist_steps,
		is_async=True,
		flight_name=flight_name,
	)
	return {"status": "enqueued"}


@frappe.whitelist()
def get_flight_document_content(file_name):
	"""Demo: Files API — retrieve raw content of an uploaded file by name.

	Usage:
	  file = frappe.get_doc("File", "boarding-pass-template.pdf")
	  content = file.get_content()
	"""
	file_doc = frappe.get_doc("File", file_name)
	content = file_doc.get_content()
	frappe.errprint(f"[airplane_flight] retrieved file {file_name!r}, size={len(content)} bytes")
	return {"file_name": file_name, "size": len(content)}

def update_ticket_gates(flight, gate):
	tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight}, pluck="name")
	for ticket_name in tickets:
		frappe.db.set_value("Airplane Ticket", ticket_name, "source_airport_gate", gate)


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.status = "Completed"

	def _enqueue_gate_change_update(self):
		previous = self.get_doc_before_save()
		if not previous:
			return
		if previous.source_airport_gate != self.source_airport_gate:
			frappe.enqueue(
				method=update_ticket_gates,
				is_async=True,
				flight=self.name,
				gate=self.source_airport_gate
			)

	def on_update(self):
		self._enqueue_gate_change_update()

	def on_update_after_submit(self):
		self._enqueue_gate_change_update()
