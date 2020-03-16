# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Inventory Force Date',
    'version': '13.0.1.0',
    'sequence': 1,
    'category': 'Stock',
    'description':
        """
            odoo applicatation module will help to pass force date from inventory Adjustment to move and quant from.

Inventory Force Date
odoo Inventory Force Date
odoo Inventory Date
odoo Inventory Transfer Date
odoo Inventory stock moves Date
odoo Inventory quants Date
odoo Inventory Dates
Inventory force date 
Odoo inventory force date 
For Helping force fully transfer date in move line.
Odoo For Helping force fully transfer date in move line.
This module used to stock inventory transfer date to move line .
Odoo This module used to stock inventory transfer date to move line .
Manage stock inventory 
Odoo manage stock inventory 
Stock move line 
Odoo stock move line 
Manage stock move line 
Odoo manage stock move line 
Manage inventory force date 
Odoo manage inventory force date 
Transfer inventory in move line 
Odoo transfer in move line 
Manage inventory move line 
Odoo manage inventory move line 
Manage stock 
Odoo manage stock 
Product inventory force date 
Odoo product inventory force date 
Manage inventory 
Odoo manage inventory 
    """,
    'summary': 'odoo app will force Inventory date to stock moves into inventory adjustment',
    'depends': ['stock'],
    'data': [
                'views/stock_inventory_view.xml',
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':25.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
