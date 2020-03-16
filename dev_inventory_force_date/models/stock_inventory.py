# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://devintellecs.com>).
#
##############################################################################

from odoo import models, fields, api, _


class stock_inventory(models.Model):
    _inherit = 'stock.inventory'
    
    
    for_date = fields.Datetime('Force Date')
    
    def action_validate(self):
        res = super(stock_inventory,self).action_validate()
        if self.for_date:
            for line in self.move_ids:
                line.date = self.for_date
                for l in line.move_line_ids:
                    l.date = self.for_date
        return res
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
