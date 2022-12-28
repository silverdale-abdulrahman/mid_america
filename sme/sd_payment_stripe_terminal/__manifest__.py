# -*- coding: utf-8 -*-
{
    'name': "Stripe Terminal For Invoice/Quotation",
    'summary': """
        Integrate Stripe Terminal Payment with Odoo. With this module, you can pay invoice and sale order through Stripe Payment Terminal.
    """,

    'description': """
     This module help you to integrate Stripe Terminal Payment with Odoo. With this module, you can pay invoice and sale order through stripe payment terminal.
    """,
    'author': "Silverdale",
    'website': "https://www.silverdaletech.com/",
    "license": "Other proprietary",
    'version': '2206',
    'category': 'Payment',
    'depends': ['payment','sale_management','account_payment'],
    'external_dependencies': {

        'python': ['stripe'],

    },
    'data': [
        'security/ir.model.access.csv',
        'security/stripe_security.xml',
        'views/payment_acquirer.xml',
        'views/payment_views.xml',
        'views/sd_payment_stripe_terminal.xml',
        'views/templates.xml',
        'data/payment_acquirer_data.xml',
        'views/account_move_report.xml',
        'views/credit_note_stripe.xml',
        'views/invoice_portal_template.xml',
        'data/refund_payment.xml',


    ],

    'images': ['static/description/icon.png'],

    'installable': True,
    'auto_install': False,
    'application': True,
    "post_init_hook": "create_missing_journal_for_acquirers",
}
