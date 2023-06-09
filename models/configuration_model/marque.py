# -*- coding: utf-8 -*-

from odoo import models, fields, api

class fleet_vehicle_brand(models.Model):
    _name = "fleet.vehicle.brand"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Nom Modèle", required=True)
    code = fields.Char("Code Modèle")
