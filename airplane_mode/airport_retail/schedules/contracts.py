import frappe 


def update_contract_status():
    contracts = frappe.get_all("Airport Shop Rental Contract", pluck="name")
    for contract_name in contracts:
        contract = frappe.get_doc("Airport Shop Rental Contract", contract_name)
        contract._update_status()
        contract.save()
