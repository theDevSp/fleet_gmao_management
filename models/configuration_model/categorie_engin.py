# -*- coding: utf-8 -*-

from odoo import models, fields

class FleetVehicleCategory(models.Model):
	_name = 'fleet.vehicle.category'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char('Nom', required=True)
	note = fields.Text('Description')
