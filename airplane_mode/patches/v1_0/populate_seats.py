import frappe 

def execute():
    tickets = frappe.get_list("Airplane Ticket", filters={"seat": None})
    for ticket_data in tickets:
        ticket = frappe.get_doc("Airplane Ticket", ticket_data.name)
        ticket.set_seat_number()
        ticket.flags.ignore_validate_update_after_submit=True
        ticket.save()

