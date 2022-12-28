# -*- coding: utf-8 -*-
# from odoo import http


# class SaleOrderExt(http.Controller):
#     @http.route('/sale_order_ext/sale_order_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_ext/sale_order_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_ext.listing', {
#             'root': '/sale_order_ext/sale_order_ext',
#             'objects': http.request.env['sale_order_ext.sale_order_ext'].search([]),
#         })

#     @http.route('/sale_order_ext/sale_order_ext/objects/<model("sale_order_ext.sale_order_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_ext.object', {
#             'object': obj
#         })
