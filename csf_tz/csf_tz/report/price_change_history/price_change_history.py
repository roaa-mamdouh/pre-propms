# Copyright (c) 2022, Aakvatech and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns(filters)

	data = get_data(filters)
	
	if len(data) == 0:
		frappe.msgprint("<strong>No record found, Please check you filters</strong>")
		return
	
	return columns, data

def get_data(filters):
	conditions = get_conditions(filters)

	return frappe.db.sql("""
		SELECT pr.posting_date as date, pi.item_code as item_code, pi.item_name as item_name,
			pi.price_list as price_list, pi.old_price as old_price, pi.new_price as new_price
		FROM `tabPrice Change Request` pr 
		INNER JOIN `tabPrice Change Request Detail` pi ON pr.name = pi.parent
		WHERE pr.docstatus = 1 {conditions}
	""".format(conditions=conditions), filters, as_dict=1
	)
	
def get_conditions(filters):
	conditions = " AND pr.company = %(company)s "

	if filters.item:
		conditions += " AND pi.item_code = %(item)s "

	if filters.price_list:
		conditions += " AND pi.price_list = %(price_list)s "

	if filters.from_date:
		conditions += " AND pr.posting_date >= %(from_date)s "
		
	if filters.to_date:
		conditions += " AND pr.posting_date <= %(to_date)s "

	return conditions

def get_columns(filters):
	return [
		{"fieldname": "date", "fieldtype": "Date", "label": _("Date"), "width": "110px"},
		{"fieldname": "item_code", "fieldtype": "Link", "options": "Item", "label": _("Item Code"), "width": "170px"},
		{"fieldname": "item_name", "fieldtype": "Data", "label": _("Item Name"), "width": "200px"},
		{"fieldname": "price_list", "fieldtype": "Link", "options": "Price List", "label": _("Price List"), "width": "170px"},
		{"fieldname": "old_price", "fieldtype": "Currency", "label": _("Old Price"), "width": "100px"},
		{"fieldname": "new_price", "fieldtype": "Currency", "label": _("New Price"), "width": "100px"}
	]