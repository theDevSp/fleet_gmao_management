# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FleetVehicleModification(models.Model):
	_name = 'fleet.vehicle.modification'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	vehicle_id = fields.Many2one('fleet.vehicle', 'Engin')
	related_vehicle_id = fields.Many2one('fleet.vehicle', 'Engin rattaché')
	date = fields.Date('Date')