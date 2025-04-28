# -*- coding: utf-8 -*-
# from odoo import http


# class LegalCompliance(http.Controller):
#     @http.route('/legal_compliance/legal_compliance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/legal_compliance/legal_compliance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('legal_compliance.listing', {
#             'root': '/legal_compliance/legal_compliance',
#             'objects': http.request.env['legal_compliance.legal_compliance'].search([]),
#         })

#     @http.route('/legal_compliance/legal_compliance/objects/<model("legal_compliance.legal_compliance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('legal_compliance.object', {
#             'object': obj
#         })

