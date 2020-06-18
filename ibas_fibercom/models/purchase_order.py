from odoo import fields, models, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    prepared_by_id = fields.Many2one('hr.employee', string="Prepared By")
    approved_by_id = fields.Many2one('hr.employee', string="Approved By")
    noted_by_id = fields.Many2one('hr.employee', string="Noted By")
    requested_by_id = fields.Many2one('hr.employee', string='Requested by')
    
    @api.onchange('prepared_by_id','approved_by_id','requested_by_id')
    def _get_signatory_details(self):
        if not self.prepared_by:
            self.prepared_by_designation = self.prepared_by_id.job_id.name
        if not self.approved_by:
            self.approved_by_designation = self.approved_by_id.job_id.name
        if not self.requested_by:
            self.requested_by_designation = self.requested_by_id.job_id.name
        