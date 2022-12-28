# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Message(models.Model):
    _inherit = 'mail.message'

    @api.model
    def _search_needaction(self, operator, operand):
        """
        **Override the method to include the current company in
        domain if company based notification is activated
        """
        company_based_notifications = self.env['ir.config_parameter'].sudo().get_param(
            'sd_company_mail.company_based_notifications')
        if company_based_notifications == 'True':
            is_read = False if operator == '=' and operand else True
            company_id = self.env.company.id
            notification_ids = self.env['mail.notification']._search(
                [('res_partner_id', '=', self.env.user.partner_id.id), ('is_read', '=', is_read),
                 ('company_id', '=', company_id)])
            return [('notification_ids', 'in', notification_ids)]
        else:
            return super(Message, self)._search_needaction(operator, operand)

    def get_company(self):
        company_based_notifications = self.env['ir.config_parameter'].sudo().get_param(
            'sd_company_mail.company_based_notifications')
        company = False
        if company_based_notifications == 'True' and self.notification_ids:
            notif = self.notification_ids[0]
            if notif.company_id:
                company = notif.company_id.id
        return company
