# -*- coding: utf-8 -*-
{
    'name': "Data Import",
    'summary': "Data Import ",
    'description': """
                
                """,
    'author': "SilverDaleTech",
    'website': "https://www.silverdaletech.com",
    'category': 'Tools',
    'version': '12.0.2052',
    'license': 'AGPL-3',

    'depends': ['base','product'],
    'data': [

        'security/ir.model.access.csv',
        'wizard/data_import_view.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
}
