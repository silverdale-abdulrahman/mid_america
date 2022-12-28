# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.
import pdb

from odoo import models, fields, api, _
from lxml import etree
from datetime import date, datetime, timedelta


class sale_order(models.Model):

    """Adds the fields for options of the customer order delivery"""

    _inherit = "sale.order"
    _description = 'Sale Order'

    customer_order_delivery_date = fields.Date(string='Customer Delivery Date', compute='_get_customer_order_delivery_date')
    customer_order_delivery_comment = fields.Text(string='Delivery Comment', translate=True)
    payment_delivery_interval = fields.Selection(string='Delivery Interval', selection=[
         ('may', 'May'),
         ('june', 'June'),
         ('early_july', 'Early July'),
         ('late_july', 'Late July'),
         ('july', 'July'),
         ('early_august', 'Early August'),
         ('late_august', 'Late August'),
         ('august', 'August'),
         ('september', 'September'),
         ])
    # TODO from sale order delivery
    commitment_date = fields.Datetime(
        string=' Delivery Date', compute='compute_delivery_date')

    @api.depends('customer_order_delivery_date')
    def compute_delivery_date(self):
        for rec in self:
            if rec.customer_order_delivery_date:
                rec.commitment_date = rec.customer_order_delivery_date
            else:
                rec.commitment_date = None
    # TODO END 
    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        res = super(sale_order, self).fields_view_get(view_id=view_id,
                                                      view_type=view_type, toolbar=toolbar, submenu=False)
        if res:
            doc = etree.XML(res['arch'])
            if view_type == 'form':
                is_customer_order_delivery_date_feature = False
                is_customer_order_delivery_comment_feature = False

                search_websites = self.env['website'].search([('id', '!=', False)])
                for setting in search_websites:
                    if setting.is_customer_order_delivery_date_feature:
                        is_customer_order_delivery_date_feature = True

                    if setting.is_customer_order_delivery_comment_feature:
                        is_customer_order_delivery_comment_feature = True

                if is_customer_order_delivery_date_feature:
                    for node in doc.xpath("//page[@class='delivery_date']"):
                        node.set('string', '')

                if is_customer_order_delivery_comment_feature:
                    for node in doc.xpath("//field[@name='customer_order_delivery_comment']"):
                        node.set('style', 'display:none')

                res['arch'] = etree.tostring(doc)
        return res

    @api.depends('payment_delivery_interval')
    def _get_customer_order_delivery_date(self):
        for rec in self:
            date_order = date.today()
            if rec.payment_delivery_interval:
                year = date.today().year
                if rec.payment_delivery_interval == 'early_july':
                    d = date(year, 6, 30)
                    next_monday = rec.next_weekday(d, 0)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
                    date_order = next_monday
                elif rec.payment_delivery_interval == 'late_july':
                    d = date(year, 7, 1)
                    next_monday = rec.next_weekday2(d, 0)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
                    date_order = next_monday
                elif rec.payment_delivery_interval == 'early_august':
                    d = date(year, 7, 31)
                    next_monday = rec.next_weekday(d, 0)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
                    date_order = next_monday
                elif rec.payment_delivery_interval == 'late_august':
                    d = date(year, 8, 1)
                    next_monday = rec.next_weekday2(d, 0)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
                    date_order = next_monday
                elif rec.payment_delivery_interval == 'may':
                    date_order = date(year, 5, 31)
                elif rec.payment_delivery_interval == 'june':
                    date_order = date(year, 6, 30)
                elif rec.payment_delivery_interval == 'july':
                    date_order = date(year, 7, 31)
                elif rec.payment_delivery_interval == 'august':
                    date_order = date(year, 8, 31)
                elif rec.payment_delivery_interval == 'september':
                    date_order = date(year, 9, 30)

                rec.customer_order_delivery_date = date_order
            else:
                rec.customer_order_delivery_date = None

    def next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return d + timedelta(days_ahead)

    def next_weekday2(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 21
        return d + timedelta(days_ahead)



