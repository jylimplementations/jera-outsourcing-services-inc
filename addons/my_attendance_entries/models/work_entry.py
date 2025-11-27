from odoo import models, api

class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    @api.model
    def action_reset_work_entries(self):
        res = super().action_reset_work_entries()

        attendances = self.env['hr.attendance'].search([])
        for att in attendances:
            employee = att.employee_id
            calendar = employee.resource_calendar_id

            if not calendar:
                continue  # skip if no calendar assigned

            # Get working hours from calendar
            # Simplified: assume one interval per day
            work_hours = calendar.attendance_ids.filtered(
                lambda a: a.dayofweek == str(att.check_in.weekday())
            )
            if not work_hours:
                continue

            start_hour = min(work_hours.mapped('hour_from'))
            end_hour = max(work_hours.mapped('hour_to'))

            # Apply buffer: 1 hour before and after
            buffer_start = start_hour
            buffer_end = end_hour

            start = att.check_in
            end = att.check_out

            # Regular block
            regular_start = start.replace(hour=int(start_hour), minute=0)
            regular_end = start.replace(hour=int(end_hour), minute=0)
            if start < regular_end and end > regular_start:
                self.create({
                    'employee_id': employee.id,
                    'date_start': max(start, regular_start),
                    'date_stop': min(end, regular_end),
                    'work_entry_type_id': self.env.ref('hr_work_entry.work_entry_type_attendance').id,
                })

            # Overtime block (after buffer_end + 1 hour)
            overtime_start = start.replace(hour=int(end_hour) + 1, minute=0)
            if end > overtime_start:
                self.create({
                    'employee_id': employee.id,
                    'date_start': max(start, overtime_start),
                    'date_stop': end,
                    'work_entry_type_id': self.env.ref('my_attendance_entries.work_entry_type_overtime').id,
                })

            # Night shift block
            night_start = start.replace(hour=22, minute=0)
            if end.hour >= 22 or start.hour < 6:
                self.create({
                    'employee_id': employee.id,
                    'date_start': max(start, night_start),
                    'date_stop': end,
                    'work_entry_type_id': self.env.ref('my_attendance_entries.work_entry_type_night').id,
                })

        return res
