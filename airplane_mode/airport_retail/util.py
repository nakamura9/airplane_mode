import frappe
from dateutil.relativedelta import relativedelta
import datetime

def get_current_lease(shop, date=None):
    if not date:
        date = frappe.utils.nowdate()
    leases = frappe.get_all("Airport Shop Rental Contract", filters={
        "shop": shop,
        "contract_start_date": ("<=", date),
        "contract_end_date": (">=", date),
        "active": True
    })
    if not leases:
        return None 
    
    return frappe.get_doc("Airport Shop Rental Contract", leases[0].name)


def get_rent_due(lease):
    if isinstance(lease, str):
        lease = frappe.get_doc("Airport Shop Rental Contract", lease)

    total_due = lease.security_deposit
    months_since_contract_start = relativedelta(lease.contract_start_date, datetime.date.today()).months
    total_due += (lease.monthly_rent * months_since_contract_start)
    
    payments = frappe.get_all("Airport Rent Payment", filters={
        "docstatus": 1,
        "lease": lease.name
    }, fields="amount_paid")

    for pmt in payments:
        total_due -= pmt.amount_paid

    return total_due