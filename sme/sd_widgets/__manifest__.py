# -*- coding: utf-8 -*-
{
    'name': "SME Widgets",
    'summary': "silverdaletech extension widgets",
    'description': """
        This widget Will let you add fields from a given model.
    """,
    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'license': 'OPL-1',
    'version': '2206',
    'category': 'Widgets',
    'depends': ['web', 'base', ],
    'data': [
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/base_extend.xml', ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
