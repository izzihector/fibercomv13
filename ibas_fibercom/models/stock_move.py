# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class IBASStockMove(models.Model):
    _inherit = 'stock.move'

    qty_available = fields.Float(
        related='product_id.qty_available', string='OnHand Quantity')
