import frappe
from airplane_mode.airport_retail.util import get_rent_due

def send_rent_reminders():
    settings = frappe.get_single("Airport Retail Settings")
    if not settings.enable_automated_rent_reminders:
        return

    active_leases = frappe.get_all(
        "Airport Shop Rental Contract", 
        filters={
            "active": True, 
            "status": ["in", ["Started", "Pending"]]
        },
        fields=["shop", "tenant", "name"])
    for lease in active_leases:
        rent_due = get_rent_due(lease.name)
        tenant = frappe.get_doc("Airport Tenant", lease.tenant)

        if rent_due:
            content = f"""
<p>Dear {tenant.tenant_name},</p>

<p>This is a friendly reminder that rent is due for your shop at <strong>{lease.shop}</strong>.</p>

<table style="border-collapse: collapse; margin: 16px 0;">
    <tr>
        <td style="padding: 4px 16px 4px 0;"><strong>Contract</strong></td>
        <td>{lease.name}</td>
    </tr>
    <tr>
        <td style="padding: 4px 16px 4px 0;"><strong>Shop</strong></td>
        <td>{lease.shop}</td>
    </tr>
    <tr>
        <td style="padding: 4px 16px 4px 0;"><strong>Amount Due</strong></td>
        <td>{frappe.format_value(rent_due, {"fieldtype": "Currency"})}</td>
    </tr>
</table>

<p>Please arrange payment at your earliest convenience to avoid any disruption to your lease.</p>

<p>If you have any questions or believe this notice was sent in error, please contact the airport retail management office.</p>

<p>Thank you,<br>Airport Retail Management</p>
"""
            frappe.sendmail(
                recipients=[tenant.contact_email],
                subject=f"Rent reminder for {lease.shop}", 
                content=content
            )