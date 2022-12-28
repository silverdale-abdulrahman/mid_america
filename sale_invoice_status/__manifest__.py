# -*- coding: utf-8 -*-
{
    'name': "Sale Invoice Payment Status",
    'summary': "Sale order invoice payment status",
    'description': """
                SP_2112,
                H607,
                T3303, T6132
                """,
    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'category': 'Tools',
    'version': '14.0',
    'license': 'AGPL-3',
    'depends': ['base', 'sale'],
    'data': [

        'views/sale_order_inherit.xml',
    ],

    
    'application': True,
    'installable': True,
    'auto_install': False,
}
