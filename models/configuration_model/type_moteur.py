from odoo import models, fields, api

class type_moteur(models.Model):
	_name = 'fleet.vehicle.motor.type'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char('Nom Type')
	note = fields.Text('Description')
