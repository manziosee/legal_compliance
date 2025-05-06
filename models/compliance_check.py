from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ComplianceCheck(models.Model):
    _name = 'compliance.check'
    _description = 'Compliance Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'check_date desc'

    name = fields.Char(string='Reference', default=lambda self: _('New'), readonly=True)
    rule_id = fields.Many2one('compliance.rule', string='Rule', required=True, ondelete='cascade')
    category_id = fields.Many2one(related='rule_id.category_id', string='Category', store=True)
    department = fields.Selection(related='rule_id.department', string='Department', store=True)
    check_date = fields.Date(string='Check Date', default=fields.Date.today, required=True)
    responsible_id = fields.Many2one('res.users', string='Responsible', required=True, default=lambda self: self.env.user)
    result = fields.Selection([
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('partial', 'Partially Compliant'),
    ], string='Result', required=True)
    notes = fields.Text(string='Notes')
    document_ids = fields.One2many('compliance.document', 'check_id', string='Documents')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('compliance.check') or _('New')
        
        check = super(ComplianceCheck, self).create(vals)
        
        # Update last check date on the rule
        if check.rule_id:
            check.rule_id.write({
                'last_check_date': check.check_date,
                'alert_sent': False,
            })
        
        return check

    def action_create_document(self):
        self.ensure_one()
        return {
            'name': _('Upload Compliance Document'),
            'type': 'ir.actions.act_window',
            'res_model': 'compliance.document',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_check_id': self.id,
                'default_rule_id': self.rule_id.id,
            },
        }