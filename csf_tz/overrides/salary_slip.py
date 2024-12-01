import frappe

try:
    from hrms.payroll.doctype.salary_slip.salary_slip import (
        SalarySlip as _SalarySlip,
    )  # version-14

except ImportError:
    from erpnext.payroll.doctype.salary_slip.salary_slip import (
        SalarySlip as _SalarySlip,
    )  # version-13
from frappe.utils import cint, getdate, nowdate, add_days

class SalarySlip(_SalarySlip):
    def get_working_days_details(self, *args, **kwargs):
        result = super().get_working_days_details(*args, **kwargs)

        fixed_working_days = get_fixed_working_days()
        if fixed_working_days is None:
            return result

        self.total_working_days = min(fixed_working_days, self.total_working_days)
        self.payment_days = min(fixed_working_days, self.payment_days)
        return result

    def calculate_lwp_or_ppl_based_on_leave_application(self, holidays, working_days, *args, **kwargs):
        fixed_working_days = get_fixed_working_days()
        if fixed_working_days is not None:
            working_days = min(fixed_working_days, working_days)

        return super().calculate_lwp_or_ppl_based_on_leave_application(holidays, working_days, *args, **kwargs)

    def get_payment_days(self, *args, **kwargs):
        fixed_working_days = get_fixed_working_days()
        if fixed_working_days is None:
            return super().get_payment_days(*args, **kwargs)

        self.total_working_days = min(fixed_working_days, self.total_working_days)
        payment_days = super().get_payment_days(*args, **kwargs)
        return min(fixed_working_days, payment_days)
    
    def get_unmarked_days(self, include_holidays_in_total_working_days):
        unmarked_days = self.total_working_days
        joining_date, relieving_date = frappe.get_cached_value(
			"Employee", self.employee, ["date_of_joining", "relieving_date"]
		)
        start_date = self.start_date
        end_date = self.end_date

        if joining_date and (getdate(self.start_date) < joining_date <= getdate(self.end_date)):
            start_date = joining_date
            unmarked_days = self.get_unmarked_days_based_on_doj_or_relieving(
                unmarked_days,
                include_holidays_in_total_working_days,
                self.start_date,
                add_days(joining_date, -1),
            )

        if relieving_date and (getdate(self.start_date) <= relieving_date < getdate(self.end_date)):
            end_date = relieving_date
            unmarked_days = self.get_unmarked_days_based_on_doj_or_relieving(
                unmarked_days,
                include_holidays_in_total_working_days,
                add_days(relieving_date, 1),
                self.end_date,
            )

        # exclude days for which attendance has been marked
        attendance_counts = frappe.get_all(
            "Attendance",
            filters={
                "attendance_date": ["between", [start_date, end_date]],
                "employee": self.employee,
                "docstatus": 1,
            },
            fields=["COUNT(*) as marked_days"],
        )[0].marked_days

        if attendance_counts > self.total_working_days:
            unmarked_days -= self.total_working_days
        else:
            unmarked_days -= attendance_counts
            
        return unmarked_days


def get_fixed_working_days():
    csf_tz_settings = frappe.get_cached_doc("CSF TZ Settings", "CSF TZ Settings")
    if csf_tz_settings.enable_fixed_working_days_per_month:
        return csf_tz_settings.working_days_per_month
