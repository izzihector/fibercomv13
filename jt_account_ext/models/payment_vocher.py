# -*- coding: utf-8 -*-
##############################################################################
#
#    Jupical Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Jupical Technologies(<http://www.jupical.com>).
#    Author: Jupical Technologies Pvt. Ltd.(<http://www.jupical.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models
from datetime import datetime, date


class AccountPayment(models.Model):
    _inherit = "account.payment"

    cv_number = fields.Char(string='CV Number')
    cv_date = fields.Date(string='CV date', default=fields.Date.today())
    prepared_by = fields.Char(string="Prepared By")
    verified_by = fields.Char(string="Verified By")
    approved_by = fields.Char(string="Approved By")
    recieved_by = fields.Char(string="Received By")
    invoices_ref = fields.Text(
        string='Invoices Ref', store=True, compute="_compute_invoices_ref")
    
    prepared_by_id = fields.Many2one('hr.employee', string="Prepared By")
    verified_by_id = fields.Many2one('hr.employee', string="Verified By")
    approved_by_id = fields.Many2one('hr.employee', string="Approved By")
    received_by_id = fields.Many2one('hr.employee', string="Received By")

    def get_currency_word(self):
        return self.currency_id.amount_to_text(self.amount)

    payment_invoice_ids = fields.Many2many('account.move', 'account_move_reference_rel', 'payment_id', 'move_id', string="Payment Invoices",
                                           domain="[('partner_id','=',partner_id),('type','=','in_invoice'),('state', '=', 'posted'),('invoice_payment_state','!=','paid')]")
    account_journal_ids = fields.Many2many(
        'account.move.line', 'account_move_line_reference_rel', 'payment_id', 'line_id', string="Journal Items")
    invoices_ref = fields.Text(
        string='Invoices Ref', store=True, compute="_compute_invoices_ref")

    @api.depends('payment_invoice_ids')
    def _compute_invoices_ref(self):
        for payment in self:
            payment.account_journal_ids = False
            line_ids = payment.payment_invoice_ids.mapped('line_ids').ids
            payment.account_journal_ids = [(6, 0, line_ids)]
            payment.invoices_ref = ','.join(
                payment.payment_invoice_ids.mapped('name'))
