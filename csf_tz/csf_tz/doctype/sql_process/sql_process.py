# Copyright (c) 2022, Aakvatech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SQLProcess(Document):
    def validate(self):
        self.process = []

    @frappe.whitelist()
    def get_process(self):
        process = frappe.db.sql(
            """
                select id, time, info
                from information_schema.processlist
                WHERE info IS NOT NULL
            """,
            as_dict=True,
        )
        return process

    @frappe.whitelist()
    def kill_process(self, pid):
        frappe.msgprint(
            "Killing process {}".format(pid), alert=True, indicator="orange"
        )
        try:
            frappe.db.sql("""Kill {0}""".format(pid))
        except Exception:
            frappe.msgprint("Process not found", alert=True, indicator="red")
            return False
        frappe.msgprint("Process killed", alert=True, indicator="green")
        return True
