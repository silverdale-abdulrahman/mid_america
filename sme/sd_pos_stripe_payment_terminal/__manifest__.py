# -*- coding: utf-8 -*-
{
    'name': 'Stripe Payment Terminal for POS',
    'summary': 'Integrate your POS with an Stripe payment terminal',
     'description': """
     This module help you to integrate Stripe Terminal Payment with Odoo. With this module, you can pay your POS order.
    """,
    'author': "Silverdale",
    'website': "https://www.silverdaletech.com/",
    "license": "OPL-1",
    'version': '2206',
    'category': 'Sales/Point of Sale',
    'depends': ['point_of_sale','sd_pos_payment_terminal'],
    'external_dependencies': {

        'python': ['stripe'],

    },
     'data': [
        'views/point_of_sale_assets.xml',
        'views/pos_config_views.xml',
        'views/pos_payment_method_views.xml',
    ],

    'qweb': ['static/src/xml/load_stripe_asset.xml',],

    'images': ['static/description/icon.png'],

    'installable': True,
    'auto_install': False,
    'application': True,
    # "post_init_hook": "create_missing_journal_for_acquirers",
}