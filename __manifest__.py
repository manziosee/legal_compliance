{
    'name': 'Legal Compliance Management',
    'version': '1.0',
    'summary': 'Track legal rules, ensure compliance, and avoid fines',
    'description': """
        Comprehensive legal compliance management system that tracks tax, HR, and safety regulations,
        checks business compliance, alerts about issues, and documents proof for audits.
    """,
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'category': 'Legal',
    'depends': ['base', 'mail', 'calendar', 'document'],
    'data': [
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        'data/compliance_data.xml',
        'views/compliance_category_views.xml',
        'views/compliance_rule_views.xml',
        'views/compliance_check_views.xml',
        'views/compliance_alert_views.xml',
        'views/compliance_document_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu_views.xml',
        'views/templates.xml',
    ],
    'demo': ['demo/demo.xml'],
    'assets': {
        'web.assets_backend': [
            'legal_compliance/static/src/css/compliance.css',
            'legal_compliance/static/src/js/compliance.js',
        ],
        'web.assets_qweb': [
            'legal_compliance/static/src/xml/*.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}