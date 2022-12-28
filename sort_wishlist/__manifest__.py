# -*- coding: utf-8 -*-
{
    'name': "Sort Wish List",

    'summary': """
        Sort Wish List in portal""",

    'description': """

            T3913,T3914
    """,

    'author': "Silverdale",
    'website': "http://www.silverdaletech.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Sale',
    'version': '14.0.2104.4',
    # any module necessary for this one to work correctly
    'depends': ['base','website_sale_wishlist'],

    # always loaded
    'data': [
        'views/view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
