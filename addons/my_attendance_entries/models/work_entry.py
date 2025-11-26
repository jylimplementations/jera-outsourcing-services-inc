from odoo import models, api, fields

class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    @api.model
    def create_entries_from_attendance(self, employee, date):
        """Create work entries based on attendance records."""
        day_start = fields.Datetime.to_datetime(f"{date} 00:00:00")
        day_end   = fields.Datetime.to_datetime(f"{date} 23:59:59")

        attendances = self.env['hr.attendance'].search([
            ('employee_id', '=', employee.id),
            ('check_in', '>=', day_start),
            ('check_in', '<=', day_end),
        ])

        for att in attendances:
            if att.check_in and att.check_out:
                attendance_type = self.env['hr.work.entry.type'].search([('name','=','Attendance')], limit=1)
                if attendance_type:
                    self.create({
                        'employee_id': employee.id,
                        'date_start': att.check_in,
                        'date_stop': att.check_out,
                        'work_entry_type_id': attendance_type.id,
                    })

    def action_generate_from_attendance(self):
        """Method called by the XML button."""
        for rec in self:
            self.create_entries_from_attendance(rec.employee_id, rec.date_start.date())
