from odoo import models, fields, api

class fleet_vehicle_type(models.Model):
	_name = 'fleet.vehicle.type'

	name = fields.Char('Nom Type', size=64)