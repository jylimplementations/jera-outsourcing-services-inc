from odoo import models

class HrWorkEntryGeneration(models.Model):
    _inherit = 'hr.work.entry.generation'

    def _generate_work_entries(self, from_date, to_date):
        # Run the default generation first
        res = super()._generate_work_entries(from_date, to_date)

        # Fetch attendances in the range
        attendances = self.env['hr.attendance'].search([
            ('check_in', '>=', from_date),
            ('check_out', '<=', to_date),
        ])
        for att in attendances:
            employee = att.employee_id
            start = att.check_in
            end = att.check_out

            if not (start and end and start < end):
                continue

            # Safely fetch types
            attendance_type = self.env.ref('hr_work_entry.work_entry_type_attendance', raise_if_not_found=False)
            overtime_type = self.env['hr.work.entry.type'].search([('code', '=', 'OVERTIME')], limit=1)
            night_type = self.env['hr.work.entry.type'].search([('code', '=', 'OT_NIGHT')], limit=1)

            # Regular block
            if attendance_type:
                self.env['hr.work.entry'].create({
                    'employee_id': employee.id,
                    'date_start': start,
                    'date_stop': min(end, start.replace(hour=17, minute=0)),
                    'work_entry_type_id': attendance_type.id,
                })

            # Overtime block
            if overtime_type and end.hour > 17:
                self.env['hr.work.entry'].create({
                    'employee_id': employee.id,
                    'date_start': max(start, start.replace(hour=18, minute=0)),
                    'date_stop': end,
                    'work_entry_type_id': overtime_type.id,
                })

            # Night block
            if night_type and (end.hour >= 22 or start.hour < 6):
                self.env['hr.work.entry'].create({
                    'employee_id': employee.id,
                    'date_start': max(start, start.replace(hour=22, minute=0)),
                    'date_stop': end,
                    'work_entry_type_id': night_type.id,
                })

        return res
