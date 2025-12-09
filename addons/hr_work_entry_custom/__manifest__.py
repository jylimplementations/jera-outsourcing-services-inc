{
    'name': 'HR Work Entry Custom',
    'version': '1.0',
    'depends': ['hr_work_entry'],
    'assets': {
        'web.assets_backend': [
            'hr_work_entry_custom/static/src/js/work_entry_patch.js',
        ],
    },
}
