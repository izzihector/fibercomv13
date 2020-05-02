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

    ibas_mrf_status = fields.Selection([
        ('ready', 'Ready for Release'),
        ('partial', 'Partially Withdrawn'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='MRF Status')

    availability = fields.Float(
        string='availability', related='move_id.availability')

    availability_store = fields.Float(
        related='availability', store=True, string="Forcasted Quantity")

    initial_demand = fields.Float(
        string='Initial Demand', related='move_id.product_uom_qty')

    initial_demand_store = fields.Float(
        related='initial_demand', store=True, string='Demand')

    @api.depends('state')
    def _compute_mrf_status(self):
        stock_picking = self.env['stock.picking']
        for rec in self:

            #stock_pick = stock_picking.search([('id', '=', rec.picking_id.id)])

            picking_partial = stock_picking.search([('id', '=', rec.picking_id.id), (
                'state', 'in', ('assigned', 'waiting', 'confirmed')), ('backorder_id', '!=', False)])

            picking_done = stock_picking.search(
                [('id', '=', rec.picking_id.id), ('state', '=', 'done'), ('backorder_id', '=', False)])

            picking_ready = stock_picking.search(
                [('id', '=', rec.picking_id.id), ('state', '=', 'assigned')])

            picking_cancel = stock_picking.search(
                [('id', '=', rec.picking_id.id), ('state', '=', 'cancel')])

            if picking_partial:
                for pick in picking_partial:
                    rec.ibas_mrf_status = pick.ibas_mrf_sale_order_status

            elif picking_ready:
                for pick in picking_ready:
                    rec.ibas_mrf_status = pick.ibas_mrf_sale_order_status

            elif picking_done:
                for pick in picking_done:
                    rec.ibas_mrf_status = pick.ibas_mrf_sale_order_status

            elif picking_cancel:
                for pick in picking_cancel:
                    rec.ibas_mrf_status = pick.ibas_mrf_sale_order_status

            else:
                rec.ibas_mrf_status = None
