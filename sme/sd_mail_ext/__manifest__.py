# -*- coding: utf-8 -*-
{
    "name": "SME Mail Extension",

    "summary": "Email 'From' Features",

    "description": """
        Email 'From' will contain actual sender email if it matches with the domain .
        Email 'From' will contain actual sender email Plus Email of catchall domain  if it does not matches with the domain .
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'license': 'OPL-1',
    'version': '2206',
    "category": "mail",

    "depends": [
        'mail', 'base',
    ],

    "application": False,
    "installable": True,
    "auto_install": False,
}
