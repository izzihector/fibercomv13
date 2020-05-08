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