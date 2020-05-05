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


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    requested_by = fields.Char(string="Requested by")
    approved_by = fields.Char(string="Approved by")

    def _compute_group_engineer(self):
        for order in self:
            order.group_engineer = False
            user = self.env.user
            if user and user.has_group('jt_fcom_sale_ext.group_fcom_sale_engineer'):
                order.group_engineer = True

    group_engineer = fields.Boolean(
        string='Is Engineer?', compute="_compute_group_engineer")

    @api.onchange('ibas_order_type')
    def _onchange_document_type(self):
        self._compute_group_engineer()

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        user = self.env.user
        if user and user.has_group('jt_fcom_sale_ext.group_fcom_sale_engineer'):
            res['ibas_order_type'] = 'MRF'
        return res

    def _compute_is_admin(self):
        for order in self:
            order.is_admin = False
            user = self.env.user
            if user and (user.has_group('base.group_system') or user.has_group('base.group_erp_manager') or user.has_group('sales_team.group_sale_manager')):
                order.is_admin = True

    is_admin = fields.Boolean(string='Is Admin', compute="_compute_is_admin")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self._compute_is_admin()

    @api.onchange('partner_shipping_id')
    def onchange_partner_shipping_id(self):
        for rec in self:
            if rec.partner_shipping_id:
                rec.analytic_account_id = rec.partner_shipping_id.analytic_account and rec.partner_shipping_id.analytic_account.id or False
                for line in rec.order_line:
                    line.analytic_tag_ids = [
                        (6, 0, rec.partner_shipping_id.analytic_tags.ids)]


class SaleOrderline(models.Model):

    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.order_id and self.order_id.partner_shipping_id:
            self.analytic_tag_ids = [
                (6, 0, self.order_id.partner_shipping_id.analytic_tags.ids)]


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    project_code = fields.Char(
        string='Project Code', compute='_compute_project', inverse='_inverse_project_code')
    project_area = fields.Char(
        string='Project Area', compute='_compute_project', inverse='_inverse_project_area')
    requested_by = fields.Char(
        related="sale_id.requested_by", string="Requested by")
    approved_by = fields.Char(
        related="sale_id.approved_by", string="Approved by")
    issued_by = fields.Char(string='Issued By')

    ibas_mrf_waiting_status = fields.Selection([
        ('approved', 'Approved By Customer'),
        ('permits', 'With Permits'),
        ('waiting', 'Waiting for Materials'),
    ], string='Waiting Status')

    ibas_mrf_sale_order_status = fields.Selection([
        ('ready', 'Ready for Release'),
        ('partial', 'Partially Withdrawn'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='MRF Status', compute='_compute_mrf_status')

    @api.depends('partner_id')
    def _compute_project(self):
        for rec in self:
            if rec.partner_id:
                for contact in rec.partner_id:
                    rec.project_area = contact.project_area if contact.project_area else False
                    rec.project_code = contact.project_code if contact.project_code else False
            else:
                rec.project_area = None
                rec.project_code = None

    def _inverse_project_area(self):
        for contact in self.partner_id:
            if self.partner_id:
                for rec in self:
                    contact.project_area = rec.project_area

    def _inverse_project_code(self):
        for contact in self.partner_id:
            if self.partner_id:
                for rec in self:
                    contact.project_code = rec.project_code

    # @api.onchange('ibas_mrf_waiting_status')
    # def _onchange_mrf_waiting(self):
    #    for rec in self:
    #        stock_move_line = self.env['stock.move.line'].search([('picking_id','=', rec.id)])

    #        if ibas_mrf_waiting_status:
    #            stock_move_line.

    @api.depends('state', 'move_ids_without_package.qty_available', 'move_line_ids_without_package')
    def _compute_mrf_status(self):
        #stock_picking = self.env['stock.picking']
        sale_order = self.env['sale.order']

        for rec in self:
            stock_move_line = self.env['stock.move.line'].search(
                [('picking_id', '=', rec.id)])

            # stock_pick = stock_picking.search(
            #    [('sale_id', '=', rec.sale_id.id)])

            # picking_partial = stock_picking.search([('sale_id', '=', rec.sale_id.id), (
            #    'state', 'in', ('assigned', 'waiting', 'confirmed')), ('backorder_id', '!=', False)])

            sale_partial = sale_order.browse([('picking_ids', '=', rec.id), (
                'picking_ids.state', 'in', ('assigned', 'waiting', 'confirmed')), ('picking_ids.backorder_id', '!=', False)])

            # picking_done = stock_picking.search(
            #    [('sale_id', '=', rec.sale_id.id), ('state', '=', 'done'), ('backorder_id', '=', False)])

            sale_done = sale_order.browse(
                [('picking_ids', '=', rec.id), ('picking_ids.state', '=', 'done'), ('picking_ids.backorder_id', '=', False)])

            # picking_ready = stock_picking.search(
            #    [('sale_id', '=', rec.sale_id.id), ('state', '=', 'assigned')])

            # picking_cancel = stock_picking.search(
            #    [('sale_id', '=', rec.sale_id.id), ('state', '=', 'cancel')])

            if sale_partial:
                rec.ibas_mrf_sale_order_status = 'partial'
                stock_move_line.update({'ibas_mrf_status': 'partial'})

            elif rec.state == 'assigned':
                rec.ibas_mrf_sale_order_status = 'ready'
                stock_move_line.update({'ibas_mrf_status': 'ready'})

            elif sale_done:
                rec.ibas_mrf_sale_order_status = 'done'
                stock_move_line.update({'ibas_mrf_status': 'done'})

            elif rec.state == 'cancel':
                rec.ibas_mrf_sale_order_status = 'cancel'
                stock_move_line.update({'ibas_mrf_status': 'cancel'})

            else:
                rec.ibas_mrf_sale_order_status = None

    # @api.model
    # def create(self, vals):
    #    res = super(StockPicking, self).create(vals)
    #    if res.partner_id and res.partner_id.project_code:
    #        res.project_code = res.partner_id.project_code
    #    if res.partner_id and res.partner_id.project_area:
    #        res.project_area = res.partner_id.project_area
    #    return res

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id and self.partner_id.project_code:
            self.project_code = self.partner_id.project_code
        if self.partner_id and self.partner_id.project_area:
            self.project_area = self.partner_id.project_area
