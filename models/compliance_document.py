from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ComplianceDocument(models.Model):
    _name = 'compliance.document'
    _description = 'Compliance Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Document Name', required=True)
    rule_id = fields.Many2one('compliance.rule', string='Related Rule', ondelete='cascade')
    check_id = fields.Many2one('compliance.check', string='Related Check', ondelete='cascade')
    description = fields.Text(string='Description')
    file = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string='File Name')
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
        return {
            'name': self.name,
            'type': 'ir.actions.act_url',
            'url': f'/web/content/compliance.document/{self.id}/file/{self.file_name}',
            'target': 'new',
        }

    @api.constrains('expiry_date')
    def _check_expiry_date(self):
        for doc in self:
            if doc.expiry_date and doc.expiry_date < fields.Date.today():
                raise ValidationError(_("Expiry date cannot be in the past!"))