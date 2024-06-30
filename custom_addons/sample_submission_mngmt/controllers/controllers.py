# -*- coding: utf-8 -*-
# from odoo import http


# class Sample-submission(http.Controller):
#     @http.route('/sample-submission/sample-submission', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sample-submission/sample-submission/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sample-submission.listing', {
#             'root': '/sample-submission/sample-submission',
#             'objects': http.request.env['sample-submission.sample-submission'].search([]),
#         })

#     @http.route('/sample-submission/sample-submission/objects/<model("sample-submission.sample-submission"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sample-submission.object', {
#             'object': obj
#         })
