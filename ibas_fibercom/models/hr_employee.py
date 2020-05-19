# -*- coding: utf-8 -*-

from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)


class IbasEmployee(models.Model):
    _inherit = 'hr.employee'

    first_name = fields.Char(string='First Name')
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name')

    @api.onchange('last_name', 'first_name', 'middle_name')
    def employee_name_change(self):
        vals = {}
        for rec in self:
            name = ''
            if self.first_name:
                name += rec.first_name + ' '
            if self.middle_name:
                name += rec.middle_name + ' '
            if self.last_name:
                name += rec.last_name

            vals.update({'name': name.upper()})
        self.update(vals)
