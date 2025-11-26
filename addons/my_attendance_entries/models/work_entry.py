from odoo import models, api, fields

class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    @api.model
    def create_entries_from_attendance(self, employee, date):
        """Generic example: create work entries based on attendance records."""
        day_start = fields.Datetime.to_datetime(f"{date} 00:00:00")
        day_end   = fields.Datetime.to_datetime(f"{date} 23:59:59")

        attendances = self.env['hr.attendance'].search([
            ('employee_id', '=', employee.id),
            ('check_in', '>=', day_start),
            ('check_in', '<=', day_end),
        ])

        total_hours = 0.0
        for att in attendances:
            if att.check_in and att.check_out:
                delta = att.check_out - att.check_in
                total_hours += delta.total_seconds() / 3600.0

        if total_hours > 0:
            attendance_type = self.env['hr.work.entry.type'].search([('name','=','Attendance')], limit=1)
            if attendance_type:
                self.create({
                    'employee_id': employee.id,
                    'date': date,
                    'duration': round(total_hours, 2),
                    'work_entry_type_id': attendance_type.id,
                })
