# Copyright (c) 2026, Goprime Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from airplane_mode.airport_retail.util import get_current_lease
import datetime
from dateutil.relativedelta import relativedelta

class AirportShopRentalContract(Document):
	def _set_current_lease_on_shop(self):
		lease = get_current_lease(self.shop)

		if lease:
			shop = frappe.get_doc("Airport Shop", lease.shop)
			shop.current_lease = lease.name
			shop.tenant = lease.tenant
			shop.lease_start_date = lease.contract_start_date
			shop.lease_expiry_date = lease.contract_end_date
			shop.save()

	def _update_status(self):
		if not self.active:
			return

		if self.docstatus == 2:
			self.status = "Cancelled"

		today = datetime.date.today()
		contract_start = frappe.utils.getdate(self.contract_start_date)
		contract_end  = frappe.utils.getdate(self.contract_end_date)

		if today < contract_start:
			self.status = "Pending"
		else:
			if today < contract_end:
				self.status = "Active"
			else:
				self.status = "Completed"

	def _populate_payment_schedule(self):
		# Preserve any amount_paid values already recorded, keyed by (year, month)
		existing_paid = {}
		for row in self.table_kyoi:
			row_date = frappe.utils.getdate(row.date)
			existing_paid[(row_date.year, row_date.month)] = row.amount_paid or 0

		self.table_kyoi = []

		start = frappe.utils.getdate(self.contract_start_date)
		end = frappe.utils.getdate(self.contract_end_date)
		current = start
		first = True

		while current <= end:
			amount_due = self.monthly_rent or 0
			if first:
				amount_due += self.security_deposit or 0
				first = False

			key = (current.year, current.month)
			self.append("table_kyoi", {
				"date": current,
				"amount_due": amount_due,
				"amount_paid": existing_paid.get(key, 0),
			})
			current += relativedelta(months=1)

	def validate(self):
		self._update_status()
		self._populate_payment_schedule()

	def after_save(self):
		self._set_current_lease_on_shop()

	def on_update(self):
		self._set_current_lease_on_shop()

	def before_cancel(self):
		self._update_status()
