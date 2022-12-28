# -*- coding: utf-8 -*-
{
    'name': "SD Sale Coupon",

    'summary': """
        When multiple discounts are applied, only carry out ONE and the MOST DESIREABLE one.
        Will apply only program that is highest min qty meet.
""",

    'description': """
        T44590
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",

    'category': 'sales',
    'version': '15.0',

    'depends': ['base','sale_coupon'],

    'data': [
        'views/sale_order_views.xml',
        # 'views/res_config_setting.xml',
    ],
}
