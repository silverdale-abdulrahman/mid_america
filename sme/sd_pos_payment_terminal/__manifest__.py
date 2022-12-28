# -*- coding: utf-8 -*-
{
    "name": "Silverdale: POS Payment Terminal Base",
    "summary": """
            This is base module to add Stripe payment terminal module  in POS. 
   """,
    "description": """
      This module help to enable stripe payment terminal in odoo to configure with POS.
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com/",
    "license": "OPL-1",
    'version': '2206',
    "depends": [
        "base", "point_of_sale",
    ],
    "data": [
        "views/res_config_settings_views.xml",
    ],

    "application": True,
    "installable": True,
    "auto_install": False,
}
