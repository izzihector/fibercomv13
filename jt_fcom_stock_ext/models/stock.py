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
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'

    delivery_partner_id = fields.Many2one(
        'res.partner', related='picking_id.partner_id', string="Delivery Address", store=True)
    receipt_partner_id = fields.Many2one(
        'res.partner', related='picking_id.partner_id', string="Recieve From", store=True)
    subcon = fields.Many2one(
        'res.partner', related='picking_id.subcon', string="Subcon", store=True)
    qty_available = fields.Float(
        string='qty available', related='product_id.qty_available')

    qty_available_store = fields.Float(
        related='qty_available', store=True, string="Quantity Onhand", group_operator='avg')

    ibas_mrf_waiting_status = fields.Selection([
        ('approved', 'Approved By Customer'),
        ('permits', 'With Permits'),
        ('waiting', 'Waiting for Materials'),
    ], string='Waiting Status')

    ibas_mrf_status = fields.Selection([
        ('ready', 'Ready for Release'),
        ('partial', 'Partially Withdrawn'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='MRF Status')

    availability = fields.Float(
        string='availability', related='product_id.virtual_available')

    availability_store = fields.Float(
        related='availability', store=True, string="Forcasted Quantity", group_operator='avg')

    initial_demand = fields.Float(
        string='Initial Demand', related='move_id.product_uom_qty')

    initial_demand_store = fields.Float(
        related='initial_demand', store=True, string='Demand')

    scheduled_date = fields.Datetime(string='Scheduled Date')

    # @api.depends('picking_id')
    # def _compute_scheduled_date(self):
    #    for rec in self:
    #        if self.picking_id:
    #            self.update({
    #                'scheduled_date': rec.picking_id.scheduled_date
    #            })

    @api.model
    def create(self, vals):
        res = super(StockMoveLine, self).create(vals)
        if res.picking_id and res.picking_id.scheduled_date:
            res.scheduled_date = res.picking_id.scheduled_date
        return res
