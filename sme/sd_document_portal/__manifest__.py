# -*- coding: utf-8 -*-
{
    'name': "Documents On Portal",

    'summary': "User contact documents on portal",

    'description': """

    """,

    'author': "Silverdale",
    'website': "https://www.silverdale.com",
    'license': 'OPL-1',
    
    'version': '2207',
    'category': 'Customizations',

    # any module necessary for this one to work correctly
    'depends': ['base', 'documents', 'portal', 'sd_document'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/res_config_setting_view.xml',
        'views/portal_template.xml',
        'views/res_config_setting.xml',
        'views/assets.xml',
    ],

    'application': False,
    'installable': True,
}
