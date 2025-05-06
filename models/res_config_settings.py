from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    compliance_alert_days = fields.Integer(
        string='Default Alert Days',
        config_parameter='legal_compliance.default_alert_days',
        default=7,
        help="Default number of days before compliance due date to send alerts"
    )
    
    compliance_manager_id = fields.Many2one(
        'res.users',
        string='Compliance Manager',
        config_parameter='legal_compliance.manager_id',
        help="Default user responsible for compliance oversight"
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('legal_compliance.default_alert_days', str(self.compliance_alert_days))
        self.env['ir.config_parameter'].set_param('legal_compliance.manager_id', str(self.compliance_manager_id.id or ''))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        
        res.update(
            compliance_alert_days=int(params.get_param('legal_compliance.default_alert_days', default=7)),
            compliance_manager_id=int(params.get_param('legal_compliance.manager_id', default=False)),
        )
        return res