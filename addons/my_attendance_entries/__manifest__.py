{
    'name': 'Attendance → Work Entries',
    'version': '1.0',
    'summary': 'Generate work entries from attendance records',
    'author': 'Custom Dev',
    'depends': ['hr', 'hr_payroll'],
    'data': [
        'views/work_entry_views.xml',
    ],
    'installable': True,
    'application': False,
}
