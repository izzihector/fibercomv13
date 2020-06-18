from odoo import models, fields, api

class AccountPayment(models.Model):
    _inherit = "account.payment"
    
    @api.onchange('payment_invoice_ids')
    def _get_invoice_details(self):
        total_amount_due = 0
        cv_number = ""
        reference = ""
        for invoice in self.payment_invoice_ids:
            total_amount_due += invoice.amount_residual_signed
            if not reference:
                reference = invoice.ref
            else:
                reference += ", %s" % (invoice.ref)
            if not cv_number:
                cv_number = invoice.name
            else:
                cv_number += ", %s" % (invoice.name)
        self.amount = total_amount_due
        self.communication = reference
        self.cv_number = cv_number