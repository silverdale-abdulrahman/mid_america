# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
import pdb
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute

_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(WebsiteSale):

    @http.route([
        '''/category''',
        # '''/shop/page/<int:page>''',
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop_category(self, page=0, category=None, search='', ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        if page > 1:
            keep = QueryURL('/shop/page/%s' % page, category=category and int(category), search=search,
                            attrib=attrib_list, order=post.get('order'))
        else:
            keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list,
                            order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)

        search_product = Product.search(domain, order=self._get_search_order(post))
        website_domain = request.website.website_domain()
        # categs_domain = [('parent_id', '=', False)] + website_domain
        categs_domain =  website_domain
        if search:
            search_categories = Category.search(
                [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        offset = pager['offset']
        products = search_product[offset: offset + ppg]

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        }
        if category:
            values['main_object'] = category

        request.session['previous_url'] = keep()
        return request.render("website_sale_ext.categories", values)

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        # keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list,
        #                 order=post.get('order'))
        if page > 1:
            keep = QueryURL('/shop/page/%s' % page, category=category and int(category), search=search,
                            attrib=attrib_list, order=post.get('order'))
        else:
            keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list,
                            order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)

        search_product = Product.search(domain, order=self._get_search_order(post))
        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search(
                [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        offset = pager['offset']
        products = search_product[offset: offset + ppg]

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        }
        if category:
            values['main_object'] = category

        request.session['previous_url'] = keep()
        return request.render("website_sale.products", values)

    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        """
        Main cart management + abandoned cart revival
        access_token: Abandoned cart SO access token
        revive: Revival method when abandoned cart. Can be 'merge' or 'squash'
        """
        previous_url = request.session.get('previous_url')

        order = request.website.sale_get_order()
        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()
        values = {'previous_url': previous_url}
        if access_token:
            abandoned_order = request.env['sale.order'].sudo().search([('access_token', '=', access_token)], limit=1)
            if not abandoned_order:  # wrong token (or SO has been deleted)
                raise NotFound()
            if abandoned_order.state != 'draft':  # abandoned cart already finished
                values.update({'abandoned_proceed': True})
            elif revive == 'squash' or (revive == 'merge' and not request.session.get(
                    'sale_order_id')):  # restore old cart or merge with unexistant
                request.session['sale_order_id'] = abandoned_order.id
                return request.redirect('/shop/cart')
            elif revive == 'merge':
                abandoned_order.order_line.write({'order_id': request.session['sale_order_id']})
                abandoned_order.action_cancel()
            elif abandoned_order.id != request.session.get(
                    'sale_order_id'):  # abandoned cart found, user have to choose what to do
                values.update({'access_token': abandoned_order.access_token})

        #calculate min order price
        carrier_id = order.carrier_id
        if carrier_id:
            carrier_id = int(carrier_id)
        if order:
            order._check_carrier_quotation(force_carrier_id=carrier_id)
        print(order.carrier_id,'carrier')
        # if not all(l.product_id.categ_id.id in order.carrier_id.categ_ids.ids for l in order.order_line):
        if sum(order.order_line.filtered(lambda m: m.product_id.is_shipment_product == False and (m.product_id.categ_id.id not in m.order_id.carrier_id.categ_ids.ids)).mapped('price_unit')) > 0:
            without_shipping_order = order.amount_total - order.amount_delivery
            if order.website_id.company_id.country_id.id == order.partner_shipping_id.country_id.id:
                if order.website_id.domestic_min_order > without_shipping_order:
                    values['min_order_msg'] = "The minimum order price required on domestic orders is ${}".format(order.website_id.domestic_min_order)
            else:
                if order.website_id.outside_domestic_min_order > without_shipping_order:
                    values['min_order_msg'] = "The minimum order price required outside domestic orders is ${}".format(order.website_id.outside_domestic_min_order)
            if not order.partner_shipping_id.country_id.id:
                values['min_order_msg'] = "The minimum order price required on domestic orders is ${} \n The minimum order price required outside domestic orders is ${}".format(order.website_id.domestic_min_order,order.website_id.outside_domestic_min_order)
        #########

        values.update({
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': [],
        })
        if order:
            order.order_line.filtered(lambda l: not l.product_id.active).unlink()
            _order = order
            if not request.env.context.get('pricelist'):
                _order = order.with_context(pricelist=order.pricelist_id.id)
            values['suggested_products'] = _order._cart_accessories()

        if post.get('type') == 'popover':
            # force no-cache so IE11 doesn't cache this XHR
            return request.render("website_sale.cart_popover", values, headers={'Cache-Control': 'no-cache'})

        return request.render("website_sale.cart", values)

    @http.route(['/shop/payment'], type='http', auth="public", website=True, sitemap=False)
    def payment(self, **post):
        """ Payment step. This page proposes several payment means based on available
        payment.acquirer. State at this point :

         - a draft sales order with lines; otherwise, clean context / session and
           back to the shop
         - no transaction in context / session, or only a draft one, if the customer
           did go to a payment.acquirer website but closed the tab without
           paying / canceling
        """
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        render_values = self._get_shop_payment_values(order, **post)
        render_values['only_services'] = order and order.only_services or False

        if render_values['errors']:
            render_values.pop('acquirers', '')
            render_values.pop('tokens', '')



        
        # Calculate min order price
        
        if not sum(order.order_line.filtered(lambda m: m.product_id.is_shipment_product == False and (m.product_id.categ_id.id not in m.order_id.carrier_id.categ_ids.ids)).mapped('price_unit')) > 0:
            render_values['min_order_msg'] = ""
            # assert order.partner_id.id != request.website.partner_id.id
            return request.render("website_sale.payment", render_values)
        
        render_values['min_order_msg'] = ""
        if sum(order.order_line.filtered(lambda m: m.product_id.is_shipment_product == False and (
                m.product_id.categ_id.id not in m.order_id.carrier_id.categ_ids.ids)).mapped('price_unit')) > 0:
            without_shipping_order = order.amount_total - order.amount_delivery
            if order.website_id.company_id.country_id.id == order.partner_shipping_id.country_id.id:
                if order.website_id.domestic_min_order > without_shipping_order:
                    render_values['min_order_msg'] = "The minimum order price required on domestic orders is ${}".format(order.website_id.domestic_min_order)
                    return request.render("website_sale_ext.payment", render_values)
            else:
                if order.website_id.outside_domestic_min_order > without_shipping_order:
                    render_values['min_order_msg'] = "The minimum order price  required outside domestic orders is ${}".format(order.website_id.outside_domestic_min_order)
                    return request.render("website_sale_ext.payment", render_values)
            if not order.partner_shipping_id.country_id.id:
                render_values['min_order_msg'] = "The minimum order price required on domestic orders is ${} \n The minimum order price required outside domestic orders is ${}".format(order.website_id.domestic_min_order,order.website_id.outside_domestic_min_order)

            assert order.partner_id.id != request.website.partner_id.id
        
        return request.render("website_sale.payment", render_values)

