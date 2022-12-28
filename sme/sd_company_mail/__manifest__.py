# -*- coding: utf-8 -*-
{
    'name': "SME Company Based Notifications",

    'summary': "Company Based User Notifications",

    'description': """
        Separate the user's notifications based on company
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'license': 'OPL-1',
    'version': '2206',
    'category': 'Discuss',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 'mail', 'web'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/assets.xml',
    ],

}
