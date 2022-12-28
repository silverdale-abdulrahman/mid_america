# See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo - Elavon Payment Gateway Integration with lightbox',
    'category': 'Payment',
    'summary': 'Odoo Elavon Integration',
    'version': '13.0.1.0.0',
    'license': 'LGPL-3',
    'description': ''' This module is used for integration of Elavon's credit
     card payments, refunds, and pre-authorization test T3245''',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'https://www.serpentcs.com',
    'depends': [
        'website_sale'
    ],
    'data': [
        'views/payment_views.xml',
        'views/payment_elavon_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': [
        'static/description/elavon_banner.png'
    ],
    'price': 199,
    'currency': 'EUR',
    'installable': True,
}
