# -*- coding: utf-8 -*-
{
    'name': "SME Restrict Multi-Company Checkboxes",

    'summary': "Restrict Multi-company Checkboxes based on user group",

    'description': """
         Add restrictions on multi-company checkboxes inside company selector on the basis of a user group
    """,

    'author': "Silverdale",
    'website': "http://www.silverdaletech.com",
    'license': 'OPL-1',

    'category': 'Web',
    'version': '2206',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/web_assets.xml',
    ],

}
