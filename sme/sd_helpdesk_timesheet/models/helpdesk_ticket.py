# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.depends('helpdesk_ticket_id.non_billable')
    def _compute_is_helpdesk_toggle(self):
        """
        this method will hide toggle button if non_billable toggle button on ticket form view is checked
        """
        for rec in self:
            rec.is_helpdesk_toggle = rec.helpdesk_ticket_id.non_billable


class HelpdeskTicketInherit(models.Model):
    _inherit = "helpdesk.ticket"

    non_billable = fields.Boolean(string='Non-Billable')

    @api.onchange('non_billable', 'sale_line_id')
    def onchange_non_billable(self):
        for rec in self.timesheet_ids:
            rec.is_helpdesk_toggle = self.non_billable
        if self.non_billable:
            # if self.timesheet_ids:
            # for rec in self.timesheet_ids.filtered(lambda p: p.validated_status != 'validated' or p.non_billable and p.validated_status == 'validated'):
            for rec in self.timesheet_ids.filtered(lambda p: p.validated is False or p.non_billable and p.validated):
                if not rec.timesheet_invoice_id:
                    rec.so_line = False
            if not any(timesheet.so_line for timesheet in self.timesheet_ids):
                self.sale_line_id = False
            # else:
            #     self.sale_line_id = False
        else:
            self.sale_line_id = self.project_id.sale_line_id.id
            if self.timesheet_ids:
                for rec in self.timesheet_ids.filtered(lambda p:not p.non_billable):
                    if rec.non_billable:
                        rec.so_line = False
                    else:
                    # rec.non_billable = False
                        rec.so_line = self.project_id.sale_line_id.id
