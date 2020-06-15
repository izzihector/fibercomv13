# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


import logging
_logger = logging.getLogger(__name__)


class IbasEmployee(models.Model):
    _inherit = 'hr.employee'

    first_name = fields.Char(string='First Name')
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name')

    project = fields.Char(string='Project')
    under_area_of = fields.Char(string='Under the Area of')

    home_address = fields.Char(string='Home Adress')
    personal_mobile_num = fields.Char(string='Personal Mobile Number')
    age = fields.Integer(string='Age', compute='_cal_dob')

    curr_employ_status = fields.Selection([
        ('regular', 'Regular'),
        ('project', 'Project-based'),
        ('probationary', 'Probationary'),
        ('contract', 'Contractual')
    ], string='Current Employment Status')

    hire_from = fields.Date(string='Hire From')
    hire_to = fields.Date(string='Hire To')
    hire_date = fields.Date(string='Hire Date')
    regular_date = fields.Date(string='Regular Date')
    separation_date = fields.Date(string='Separation Date')
    los = fields.Char(string='LOS', compute='_cal_los')
    cut_off_date = fields.Date(string='Cut-off Date')

    employee_number = fields.Char(string='Employee Number')
    biometric_user_id = fields.Char(string='Biometric User ID')

    tin = fields.Char(string='TIN')
    sss = fields.Char(string='SSS')
    philhealth = fields.Char(string='Philhealth')
    pagibig = fields.Char(string='Pag-IBIG')

    @api.depends('birthday')
    def _cal_dob(self):
        if self.birthday:
            years = relativedelta(date.today(), self.birthday).years

            self.age = int(years)
        else:
            self.age = 0

    @api.depends('hire_date')
    def _cal_los(self):
        if self.hire_date and not self.separation_date:
            years = relativedelta(date.today(), self.hire_date).years
            months = relativedelta(date.today(), self.hire_date).months
            day = relativedelta(date.today(), self.hire_date).days
            self.los = str(int(years)) + ' Year/s ' + \
                str(int(months)) + ' Month/s ' + str(day) + ' Day/s'

        elif self.hire_date and self.separation_date:
            sep_years = relativedelta(
                self.separation_date, self.hire_date).years
            sep_months = relativedelta(
                self.separation_date, self.hire_date).months
            sep_day = relativedelta(self.separation_date, self.hire_date).days

            self.los = str(int(sep_years)) + ' Year/s ' + \
                str(int(sep_months)) + ' Month/s ' + str(sep_day) + ' Day/s'

        else:
            self.los = ' '

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

    asset_ids = fields.One2many(
        'asset.asset', 'employee_id', string='Asset Ids')
