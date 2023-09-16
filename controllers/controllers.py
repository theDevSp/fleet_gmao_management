# -*- coding: utf-8 -*-
# from odoo import http


# class FleetGmaoManagement(http.Controller):
#     @http.route('/fleet_gmao_management/fleet_gmao_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fleet_gmao_management/fleet_gmao_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fleet_gmao_management.listing', {
#             'root': '/fleet_gmao_management/fleet_gmao_management',
#             'objects': http.request.env['fleet_gmao_management.fleet_gmao_management'].search([]),
#         })

#     @http.route('/fleet_gmao_management/fleet_gmao_management/objects/<model("fleet_gmao_management.fleet_gmao_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fleet_gmao_management.object', {
#             'object': obj
#         })
