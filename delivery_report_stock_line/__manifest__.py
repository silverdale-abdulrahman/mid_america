# -*- coding: utf-8 -*-
{
    'name': 'Delivery Reports In stock Line',
    'version': '14.1',
    "category": "Delivery Report",
    'summary': 'Making Delivery Reports In stock Line',
    'description': 'Making Delivery Reports In stock Line Model. '
                   'T4094',
    'author': 'Silverdale',
    'company': 'Silverdale',
    'maintainer': 'Silverdale',
    'website': 'https://www.silverdaletech.com',
    'depends': ['stock'],
    'data': [
             'security/ir.model.access.csv',
             'report/delivery_price_report_template.xml',
             'report/delivery_report_template.xml',
             'report/delivery_pdf.xml',
             'wizard/delivery_price_report_wizard.xml',
             'wizard/delivery_report_wizard.xml',
            ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
