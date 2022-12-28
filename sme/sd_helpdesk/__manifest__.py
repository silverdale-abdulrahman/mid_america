# -*- coding: utf-8 -*-
{
    'name': "SME Helpdesk",

    'summary': "Enable Helpdesk features develop by Silverdale.",

    'description': """
        1: Solution field on helpdesk ticket
        2: Link ticket with tasks
        3: Helpdesk timesheet
        4: Helpdesk ticket root cause 
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'license': 'OPL-1',
    'version': '2208',
    "category": 'Helpdesk',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sd_base_setup', 'helpdesk_timesheet', 'project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_res_config_setting.xml',
        'views/view_helpdesk_ticket.xml',
        'views/view_project_task.xml',
        'views/view_ticket_rootcause.xml',
        'views/helpdesk_portal_templates.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
}

