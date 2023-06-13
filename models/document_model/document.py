# -*- coding: utf-8 -*-

from odoo import models, fields

class FleetVehicleAdministratifDocuments(models.Model):
	_name = 'fleet.vehicle.administratif.documents'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char('Document', required=True)
	period_count = fields.Integer("Durée de Période")
	period_dmy = fields.Selection([('d', 'Jours'), ('m', 'Mois'), ('y', 'Années')], 'Période', default="y")
