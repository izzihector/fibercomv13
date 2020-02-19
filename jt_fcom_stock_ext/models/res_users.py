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


class ResUsers(models.Model):

    _inherit = 'res.users'

    warehouse_ids = fields.Many2many('stock.warehouse', 'allowed_warehouse_user_rel', 'warehouse_id', 'user_id', string="Allowed Warehouses", company_dependent=False, check_company=False)
    warehouse_company_ids = fields.Many2many('res.company', 'allowed_warehouse_companies_rel', 'company_id', 'user_id', string="Allowed Warehouse Companies", company_dependent=False, check_company=False)

    @api.depends('warehouse_ids')
    def _compute_flag_wh_comp_count(self):
        for user in self:
            company_ids = []
            user.flag_wh_comp_count = False
            for warehouse in user.warehouse_ids:
                if warehouse.company_id and warehouse.company_id.id not in company_ids:
                    company_ids.append(warehouse.company_id.id)
            user.warehouse_company_ids = [(6, 0, company_ids)]

    flag_wh_comp_count = fields.Boolean(string="Flag Warehouse Companies Count", store=True, compute="_compute_flag_wh_comp_count", company_dependent=False, check_company=False)
