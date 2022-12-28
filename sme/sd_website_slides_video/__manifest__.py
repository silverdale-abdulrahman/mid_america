# -*- coding: utf-8 -*-
{
    'name': "SME eLearning Document Video",

    'summary': "Link Video from documents in eLearning",

    'description': """
        1: Document Videos - eLearning Platform
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'license': 'OPL-1',
    'version': '2207',
    "category": 'eLearning',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sd_website_slides', 'documents'],

    # always loaded
    'data': [
        'views/slide_slide_views.xml',
        'views/website_slides_templates_course.xml',
        'views/assets.xml',
    ],


}

