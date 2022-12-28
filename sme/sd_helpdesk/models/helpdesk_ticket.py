# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    solution = fields.Html(string="Solution", required=False)
    task_id = fields.Many2one("project.task", 'Task')
    task_ids = fields.Many2many("project.task", string='Tasks')
    task_count = fields.Integer(compute="_compute_tasks_count")
    task_stage_ids = fields.Many2many('project.task.type', string='Tasks Stages', compute="_compute_tasks_count",
                                      store=True)
    rootcause_id = fields.Many2one('ticket.rootcause', string='Rootcause')

    @api.depends('task_ids')
    def _compute_tasks_count(self):
        for ticket in self:
            ticket.task_count = len(ticket.task_ids)
            ticket.task_stage_ids = ticket.task_ids.mapped('stage_id').ids

    @api.onchange('task_ids')
    def update_task_stage_ids(self):
        for ticket in self:
            ticket._compute_tasks_count()
            if not ticket.task_ids:
                ticket.task_stage_ids = False

    def open_tasks_view(self):
        if len(self.task_ids) > 1:
            views = 'tree,form'
            res_id = False
            domain = "[('id', 'in', %s)]" % self.task_ids.ids
        else:
            views = 'form'
            res_id = self.task_ids.id
            domain = False
        return {
            'name': _('Tasks'),
            'view_mode': views,
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
            'res_id': res_id,
            "context": {'default_ticket_ids': [(4, self.id)]},
        }

    @api.onchange('project_id')
    def update_timesheet_ids(self):
        for ticket in self:
            if ticket.project_id and self._origin and self.name:
                timesheets = self.env['account.analytic.line'].search([('helpdesk_ticket_id', '=', self._origin.id)])
                if timesheets:
                    for rec in timesheets:
                        rec.project_id = ticket.project_id.id
