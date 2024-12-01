// Copyright (c) 2022, Aakvatech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Price Change History"] = {
	"filters": [
		{
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"label": __("Company"),
			"default": frappe.defaults.get_user_default("company"),
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname": "item",
			"fieldtype": "Link",
			"options": "Item",
			"label": __("Item"),
			"reqd": 0,
			"width": "100px",
			"get_query": () => {
				return {
					filters: {
						"disabled": 0
					}
				}
			}
		},
		{
			"fieldname": "price_list",
			"fieldtype": "Link",
			"options": "Price List",
			"label": __("Price List"),
			"reqd": 0,
			"width": "100px",
			"get_query": () => {
				return {
					filters: {
						"enabled": 1
					}
				}
			}
		},
		{
			"fieldname": "from_date",
			"fieldtype": "Date",
			"label": __("From Date"),
			"reqd": 0,
			"width": "100px"
		},
		{
			"fieldname": "to_date",
			"fieldtype": "Date",
			"label": __("To Date"),
			"reqd": 0,
			"width": "100px"
		}

	]
};
