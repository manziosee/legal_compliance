from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class ComplianceRule(models.Model):
    _name = 'compliance.rule'
    _description = 'Compliance Rule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, next_check_date'

    name = fields.Char(string='Rule Name', required=True, translate=True)
    description = fields.Text(string='Description')
    category_id = fields.Many2one('compliance.category', string='Category', required=True)
    jurisdiction = fields.Char(string='Jurisdiction', help="Geographical area where this rule applies")
    department = fields.Selection([
        ('hr', 'Human Resources'),
        ('accounting', 'Accounting/Finance'),
        ('manufacturing', 'Manufacturing'),
        ('safety', 'Health & Safety'),
        ('other', 'Other'),
    ], string='Department', required=True, default='hr')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical'),
    ], string='Priority', default='1')
    
    # Compliance details
    reference = fields.Char(string='Legal Reference')
    is_recurring = fields.Boolean(string='Recurring Compliance')
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ], string='Frequency')
    custom_frequency = fields.Integer(string='Custom Frequency (days)')
    last_check_date = fields.Date(string='Last Check Date')
    next_check_date = fields.Date(string='Next Check Date', compute='_compute_next_check_date', store=True)
    responsible_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True)
    
    # Related documents
    document_ids = fields.One2many('compliance.document', 'rule_id', string='Documents')
    check_ids = fields.One2many('compliance.check', 'rule_id', string='Compliance Checks')
    
    # Alert system
    alert_days_before = fields.Integer(string='Alert Before (days)', default=7)
    alert_sent = fields.Boolean(string='Alert Sent', default=False)
    
    @api.depends('is_recurring', 'frequency', 'custom_frequency', 'last_check_date')
    def _compute_next_check_date(self):
        for rule in self:
            if not rule.is_recurring or not rule.last_check_date:
                rule.next_check_date = False
                continue
            
            last_check = fields.Date.from_string(rule.last_check_date)
            if rule.frequency == 'daily':
                next_date = last_check + timedelta(days=1)
            elif rule.frequency == 'weekly':
                next_date = last_check + timedelta(weeks=1)
            elif rule.frequency == 'monthly':
                next_date = last_check + timedelta(days=30)
            elif rule.frequency == 'quarterly':
                next_date = last_check + timedelta(days=90)
            elif rule.frequency == 'yearly':
                next_date = last_check + timedelta(days=365)
            elif rule.frequency == 'custom' and rule.custom_frequency > 0:
                next_date = last_check + timedelta(days=rule.custom_frequency)
            else:
                next_date = False
            
            rule.next_check_date = next_date

    def action_set_draft(self):
        self.write({'state': 'draft'})

    def action_activate(self):
        self.write({'state': 'active'})

    def action_archive(self):
        self.write({'state': 'archived'})

    def action_check_compliance(self):
        self.ensure_one()
        return {
            'name': _('Check Compliance'),
            'type': 'ir.actions.act_window',
            'res_model': 'compliance.check',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_rule_id': self.id,
                'default_responsible_id': self.responsible_id.id,
            },
        }

    def action_view_checks(self):
        self.ensure_one()
        return {
            'name': _('Compliance Checks'),
            'type': 'ir.actions.act_window',
            'res_model': 'compliance.check',
            'view_mode': 'tree,form',
            'domain': [('rule_id', '=', self.id)],
            'context': {'default_rule_id': self.id},
        }

    def action_view_documents(self):
        self.ensure_one()
        return {
            'name': _('Compliance Documents'),
            'type': 'ir.actions.act_window',
            'res_model': 'compliance.document',
            'view_mode': 'tree,form',
            'domain': [('rule_id', '=', self.id)],
            'context': {'default_rule_id': self.id},
        }

    def _cron_check_compliance_due_dates(self):
        """ Check rules that are due for compliance and send alerts """
        today = fields.Date.today()
        due_rules = self.search([
            ('state', '=', 'active'),
            ('is_recurring', '=', True),
            ('next_check_date', '<=', today),
            ('alert_sent', '=', False),
        ])
        
        for rule in due_rules:
            rule._send_compliance_alert()
    
    def _send_compliance_alert(self):
        """ Send compliance alert to responsible person """
        self.ensure_one()
        if not self.responsible_id or not self.next_check_date:
            return
        
        mail_template = self.env.ref('legal_compliance.email_template_compliance_alert')
        if mail_template:
            mail_template.send_mail(self.id, force_send=True)
        
        self.write({'alert_sent': True})
        
        # Create activity for follow-up
        self.activity_schedule(
            'legal_compliance.mail_activity_compliance_check',
            date_deadline=self.next_check_date,
            summary=f'Compliance Check Due: {self.name}',
            note=f'The compliance check for {self.name} is due on {self.next_check_date}.',
            user_id=self.responsible_id.id
        )