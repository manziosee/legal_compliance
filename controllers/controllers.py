from odoo import http, fields
from odoo.http import request

class ComplianceController(http.Controller):
    
    @http.route('/compliance/check_due', auth='user', type='json')
    def check_due_compliance(self):
        """ Return count of due compliance checks """
        user = request.env.user
        Rule = request.env['compliance.rule']
        
        due_count = Rule.search_count([
            ('state', '=', 'active'),
            ('is_recurring', '=', True),
            ('next_check_date', '<=', fields.Date.today()),
            ('responsible_id', '=', user.id),
        ])
        
        return {
            'due_count': due_count,
        }
    
    @http.route('/compliance/dashboard_data', auth='user', type='json')
    def get_dashboard_data(self):
        """ Return data for compliance dashboard """
        Rule = request.env['compliance.rule']
        Check = request.env['compliance.check']
        
        # Count by status
        status_data = [
            {'name': 'Active', 'count': Rule.search_count([('state', '=', 'active')]), 'color': '2ecc71'},
            {'name': 'Draft', 'count': Rule.search_count([('state', '=', 'draft')]), 'color': '3498db'},
            {'name': 'Archived', 'count': Rule.search_count([('state', '=', 'archived')]), 'color': 'e74c3c'},
        ]
        
        # Recent checks
        recent_checks = Check.search([], limit=5, order='check_date desc')
        checks_data = [{
            'id': check.id,
            'name': check.name,
            'rule': check.rule_id.name,
            'date': check.check_date,
            'result': dict(check._fields['result'].selection).get(check.result),
        } for check in recent_checks]
        
        return {
            'status_data': status_data,
            'checks_data': checks_data,
        }