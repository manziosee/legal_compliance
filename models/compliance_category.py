from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ComplianceCategory(models.Model):
    _name = 'compliance.category'
    _description = 'Compliance Category'
    _order = 'sequence, name'

    name = fields.Char(string='Category Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    rule_ids = fields.One2many('compliance.rule', 'category_id', string='Rules')
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Category name must be unique!'),
    ]

    def toggle_active(self):
        """ Override to archive related rules when category is archived """
        res = super(ComplianceCategory, self).toggle_active()
        self.mapped('rule_ids').filtered(lambda r: r.state == 'active' and not r.active).action_archive()
        return res