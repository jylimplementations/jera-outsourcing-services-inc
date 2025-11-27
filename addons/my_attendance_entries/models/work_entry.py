from odoo import models, api

class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    @api.model
    def action_reset_work_entries(self):
        res = super().action_reset_work_entries()

        attendances = self.env['hr.attendance'].search([])
        for att in attendances:
            employee = att.employee_id
            start = att.check_in
            end = att.check_out

            # Safely fetch existing types
            attendance_type = self.env.ref('hr_work_entry.work_entry_type_attendance', raise_if_not_found=False)
            overtime_type = self.env['hr.work.entry.type'].search([('code', '=', 'OVERTIME')], limit=1)
            night_type = self.env['hr.work.entry.type'].search([('code', '=', 'OT_NIGHT')], limit=1)

            # Fallback: create if missing
            if not overtime_type:
                overtime_type = self.env['hr.work.entry.type'].create({
                    'name': 'Overtime',
                    'code': 'OVERTIME',
                    'sequence': 30,
                    'work_entry_type_category_id': self.env.ref('hr_work_entry.work_entry_type_category_attendance').id,
                })
            if not night_type:
                night_type = self.env['hr.work.entry.type'].create({
                    'name': 'Night Shift',
                    'code': 'NIGHT',
                    'sequence': 40,
                    'work_entry_type_category_id': self.env.ref('hr_work_entry.work_entry_type_category_attendance').id,
                })

            # Example: create a regular block
            if attendance_type:
                self.create({
                    'employee_id': employee.id,
                    'date_start': start,
                    'date_stop': end,
                    'work_entry_type_id': attendance_type.id,
                })

            # Example: overtime block
            if overtime_type and end.hour > 17:
                self.create({
                    'employee_id': employee.id,
                    'date_start': start.replace(hour=18, minute=0),
                    'date_stop': end,
                    'work_entry_type_id': overtime_type.id,
                })

            # Example: night block
            if night_type and (end.hour >= 22 or start.hour < 6):
                self.create({
                    'employee_id': employee.id,
                    'date_start': start.replace(hour=22, minute=0),
                    'date_stop': end,
                    'work_entry_type_id': night_type.id,
                })

        return res
