# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteStockInfo(http.Controller):
#     @http.route('/website_stock_info/website_stock_info/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_stock_info/website_stock_info/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_stock_info.listing', {
#             'root': '/website_stock_info/website_stock_info',
#             'objects': http.request.env['website_stock_info.website_stock_info'].search([]),
#         })

#     @http.route('/website_stock_info/website_stock_info/objects/<model("website_stock_info.website_stock_info"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_stock_info.object', {
#             'object': obj
#         })
