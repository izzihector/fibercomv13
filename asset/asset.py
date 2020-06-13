# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2020 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models
from odoo import tools

STATE_COLOR_SELECTION = [
    ('0', 'Red'),
    ('1', 'Green'),
    ('2', 'Blue'),
    ('3', 'Yellow'),
    ('4', 'Magenta'),
    ('5', 'Cyan'),
    ('6', 'Black'),
    ('7', 'White'),
    ('8', 'Orange'),
    ('9', 'SkyBlue')
]
STATE_SCOPE_TEAM = [
    ('0', 'Finance'),
    ('1', 'Warehouse'),
    ('2', 'Manufacture'),
    ('3', 'Maintenance'),
    ('4', 'Accounting')
]


class asset_type(models.Model):
    """ 
    Model for asset types.
    """
    _name = 'asset.type'
    _description = 'State of Type'

    name = fields.Char('State', required=True, translate=True)


class asset_state(models.Model):
    """ 
    Model for asset states.
    """
    _name = 'asset.state'
    _description = 'State of Asset'
    _order = "sequence"

    name = fields.Char('State', size=64, required=True, translate=True)
    sequence = fields.Integer(
        'Sequence', help="Used to order states.", default=1)
    state_color = fields.Selection(STATE_COLOR_SELECTION, 'State Color')
    team = fields.Selection(STATE_SCOPE_TEAM, 'Scope Team')

    def change_color(self):
        color = int(self.state_color) + 1
        if (color > 9):
            color = 0
        return self.write({'state_color': str(color)})


class asset_category(models.Model):
    _description = 'Asset Tags'
    _name = 'asset.category'

    name = fields.Char('Tag', required=True, translate=True)
    asset_ids = fields.Many2many(
        'asset.asset', id1='category_id', id2='asset_id', string='Assets')


class asset_asset(models.Model):
    """
    Assets
    """
    _name = 'asset.asset'
    _description = 'Asset'
    _inherit = ['mail.thread']

    def _read_group_state_ids(self, domain, read_group_order=None, access_rights_uid=None, team='3'):
        access_rights_uid = access_rights_uid or self.uid
        stage_obj = self.env['asset.state']
        order = stage_obj._order
        # lame hack to allow reverting search, should just work in the trivial case
        if read_group_order == 'stage_id desc':
            order = "%s desc" % order
        # write the domain
        # - ('id', 'in', 'ids'): add columns that should be present
        # - OR ('team','=',team): add default columns that belongs team
        search_domain = []
        search_domain += ['|', ('team', '=', team)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(
            search_domain, order=order, access_rights_uid=access_rights_uid)
        result = stage_obj.name_get(access_rights_uid, stage_ids)
        # restore order of the search
        result.sort(lambda x, y: cmp(
            stage_ids.index(x[0]), stage_ids.index(y[0])))
        return result, {}

    def _read_group_finance_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '0')

    def _read_group_warehouse_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '1')

    def _read_group_manufacture_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '2')

    def _read_group_maintenance_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '3')

    def _read_group_accounting_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '4')

    CRITICALITY_SELECTION = [
        ('0', 'General'),
        ('1', 'Important'),
        ('2', 'Very important'),
        ('3', 'Critical')
    ]

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id.id

    name = fields.Char('Asset Name', size=64, required=True, translate=True)
    finance_state_id = fields.Many2one(
        'asset.state', 'Finance State', domain=[('team', '=', '0')])
    warehouse_state_id = fields.Many2one(
        'asset.state', 'Warehouse State', domain=[('team', '=', '1')])
    manufacture_state_id = fields.Many2one(
        'asset.state', 'Manufacture State', domain=[('team', '=', '2')])
    maintenance_state_id = fields.Many2one(
        'asset.state', 'Maintenace State', domain=[('team', '=', '3')])
    accounting_state_id = fields.Many2one(
        'asset.state', 'Accounting State', domain=[('team', '=', '4')])
    maintenance_state_color = fields.Selection(
        related='maintenance_state_id.state_color', selection=STATE_COLOR_SELECTION, string="Colors", readonly=True)
    criticality = fields.Selection(CRITICALITY_SELECTION, 'Criticality')
    property_stock_asset = fields.Many2one(
        'stock.location', "Asset Location",
        company_dependent=True, domain=[('usage', 'like', 'asset')],
        help="This location will be used as the destination location for installed parts during asset life.",
        track_visibility='onchange')
    user_id = fields.Many2one(
        'res.users', 'User Assigned to', track_visibility='onchange')
    employee_id = fields.Many2one(
        'hr.employee', 'Assigned to', track_visibility='onchange')
    active = fields.Boolean('Active', default=True)
    asset_number = fields.Char('Asset Number', size=64)
    model = fields.Char('Model', size=64)
    serial = fields.Char('Serial no.', size=64)
    vendor_id = fields.Many2one('res.partner', 'Vendor')
    manufacturer_id = fields.Many2one('res.partner', 'Manufacturer')
    start_date = fields.Date('Start Date')
    purchase_date = fields.Date('Purchase Date')
    warranty_start_date = fields.Date('Warranty Start')
    warranty_end_date = fields.Date('Warranty End')
    image = fields.Binary("Image")
    image_small = fields.Binary("Small-sized image")
    image_medium = fields.Binary("Medium-sized image")
    category_ids = fields.Many2many(
        'asset.category', id1='asset_id', id2='category_id', string='Tags')

    _group_by_full = {
        'finance_state_id': _read_group_finance_state_ids,
        'warehouse_state_id': _read_group_warehouse_state_ids,
        'manufacture_state_id': _read_group_manufacture_state_ids,
        'maintenance_state_id': _read_group_maintenance_state_ids,
        'accounting_state_id': _read_group_accounting_state_ids,
    }

    department_id = fields.Many2one(
        'hr.department', string='Department', track_visibility='onchange')
    team = fields.Selection(STATE_SCOPE_TEAM, 'Scope Team',
                            track_visibility='onchange')

    currency_id = fields.Many2one(
        "res.currency", string="Currency", default=_default_currency)
    property_number = fields.Char('Property Number', size=64)
    part_number = fields.Char('Part Number', size=64)
    acquisition_cost = fields.Monetary('Acquisition Cost')

    property_description = fields.Char('Property Description')
    processor = fields.Char('Processor')
    memory = fields.Char('Memory')
    storage = fields.Char('Storage')
    optical_drive = fields.Char('Optical Drive')
    graphics = fields.Char('Graphics')
    display = fields.Char('Display')
    operating_system = fields.Char('Operating System')
    color = fields.Char('Color')
    inclusion = fields.Char('Inclusion')
    notes = fields.Text('Notes')

    # type
    asset_type_id = fields.Many2one('asset.type', string="Asset Type")

    # Asset Information
    item_code = fields.Char(string='Item Code')
    brand_serial_num = fields.Char(string='Brand/Serial Number')

    # Tracking
    date_released = fields.Date(string='Date Released')
    out_issued = fields.Char(string='Out Issued #')
    date_returned = fields.Date(string='Date Returned')
    in_receipt = fields.Char(string='In Receipt #')

    # Others
    remarks = fields.Char(string='Remarks')

    @api.model
    def create(self, vals):
        if 'image' in vals:
            vals['image_small'] = vals['image_medium'] = vals['image']
        return super(asset_asset, self).create(vals)

    def write(self, vals):
        if 'image' in vals:
            vals['image_small'] = vals['image_medium'] = vals['image']
        return super(asset_asset, self).write(vals)
