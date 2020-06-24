# -*- coding: utf-8 -*-
# Copyright YEAR(2019), AUTHOR(IBAS)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    bus_style = fields.Char(string='Bus. Style')
    # bs_no = fields.Char(string='B.S. No.')
    sale_no = fields.Char(string='S.O. No.')
    purchase_no = fields.Char(string='P.O. No.')
    delivery_no = fields.Char(string='D.R. No.')
    approved_by = fields.Many2one('res.users', string='Approved By')
    received_by = fields.Many2one('res.users', string='Received By')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          index=True, compute='_compute_analytic', inverse='_inverse_analytic')

    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag', string='Analytic Tags', compute='_compute_analytic_tag', inverse='_inverse_analytic_tag')

    # Analytic Account
    @api.depends('purchase_line_id')
    def _compute_analytic(self):
        for rec in self:
            if rec.purchase_line_id:
                for po in rec.purchase_line_id:
                    rec.analytic_account_id = po.account_analytic_id.id if po.account_analytic_id else False
            else:
                rec.analytic_account_id = None

    def _inverse_analytic(self):
        for po in self.purchase_line_id:
            if self.purchase_line_id:
                for rec in self:
                    po.account_analytic_id = rec.analytic_account_id.id

    # Analytic Tag
    @api.depends('purchase_line_id')
    def _compute_analytic_tag(self):
        for rec in self:
            if rec.purchase_line_id:
                for po in rec.purchase_line_id:
                    rec.analytic_tag_ids = po.analytic_tag_ids.ids if po.analytic_tag_ids else False
            else:
                rec.analytic_tag_ids = None

    def _inverse_analytic_tag(self):
        for po in self.purchase_line_id:
            if self.purchase_line_id:
                for rec in self:
                    po.analytic_tag_ids = rec.analytic_tag_ids.ids
