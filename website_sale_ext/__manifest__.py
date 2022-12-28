# -*- coding: utf-8 -*-
{
    'name': "E-commerce Extension",
    'summary': "Invoice Templates Customization",
    'description': """
                T2104,T3191,T3184,T3181,T3206,T3204,T3214,T3289,T3662,H1589, T36998
                """,
    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'category': 'Tools',
    'version': '14.0.1.3',
    'license': 'AGPL-3',
    'depends': ['website_sale', 'stock_account'],
    'data': [

        'views/templates.xml',
        'views/website_salecart_inherit.xml',
        'views/stock_picking_inherit.xml',
        'views/sale_order_inherit.xml',
        'views/shop_product_carousel_inherit.xml',
        'views/web_template_shop_address_inherit.xml',
        'views/res_config_settings_views.xml',
        'views/payment_template.xml',
        'views/product_desc.xml',
        'views/product_pricelist_view.xml',
        'views/website_visitor_views.xml',
    ],

    
    'application': True,
    'installable': True,
    'auto_install': False,
}
