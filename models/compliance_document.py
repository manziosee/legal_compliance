from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ComplianceDocument(models.Model):
    _name = 'compliance.document'
    _description = 'Compliance Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'upload_date desc'

    name = fields.Char(string='Document Name', required=True)
    rule_id = fields.Many2one('compliance.rule', string='Related Rule', ondelete='cascade')
    check_id = fields.Many2one('compliance.check', string='Related Check', ondelete='cascade')
    description = fields.Text(string='Description')
    
    # Using standard Odoo attachment fields
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')
    attachment_name = fields.Char(related='attachment_id.name', string='File Name')
    attachment_type = fields.Char(related='attachment_id.mimetype', string='Type')
    attachment_size = fields.Integer(related='attachment_id.file_size', string='Size')
    
    upload_date = fields.Date(string='Upload Date', default=fields.Date.today)
    upload_user_id = fields.Many2one('res.users', string='Uploaded By', default=lambda self: self.env.user)
    expiry_date = fields.Date(string='Expiry Date')
    is_valid = fields.Boolean(string='Is Valid', compute='_compute_is_valid', store=True)

    @api.depends('expiry_date')
    def _compute_is_valid(self):
        today = fields.Date.today()
        for doc in self:
            doc.is_valid = not doc.expiry_date or doc.expiry_date >= today

    def action_open_document(self):
        self.ensure_one()
        if self.attachment_id:
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{self.attachment_id.id}?download=true',
                'target': 'new',
            }
        raise UserError(_("No attachment found for this document"))

    @api.model
    def create(self, vals):
        if vals.get('attachment_id'):
            attachment = self.env['ir.attachment'].browse(vals['attachment_id'])
            if not vals.get('name'):
                vals['name'] = attachment.name
        return super().create(vals)