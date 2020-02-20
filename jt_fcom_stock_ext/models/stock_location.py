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


class StockLocation(models.Model):

    _inherit = 'stock.location'

    @api.model
    def create(self, vals):
        res = super(StockLocation, self).create(vals)
        warehouse_id = res.get_warehouse()
        res.warehouse_id = warehouse_id and warehouse_id.id or False
        return res

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')

    def fill_warehouse_ids(self):
        locations = self.env['stock.location'].sudo().search([('warehouse_id', '=', False)])
        for location in locations:
            warehouse_id = location.get_warehouse()
            location.warehouse_id = warehouse_id and warehouse_id.id or False
