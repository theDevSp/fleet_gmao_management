from odoo import models, fields, api

class fleet_vehicle_type(models.Model):
	_name = 'fleet.vehicle.type'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char('Nom Type', size=64, required=True)
	note = fields.Text('Description')
