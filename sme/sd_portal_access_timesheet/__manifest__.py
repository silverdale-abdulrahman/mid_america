# -*- coding: utf-8 -*-
{
    'name': "SME Portal Access: TimeSheet App",

    'summary': "Portal Access: Enable of Disable user to access Timesheet on Portal",

    'description': """
        Portal Access: Enable of Disable user to access Timesheet on Portal
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'license': 'OPL-1',
    'version': '2208',
    'category': 'Sale',

    # any module necessary for this one to work correctly
    'depends': ['base','sd_contact','hr_timesheet'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,

}
