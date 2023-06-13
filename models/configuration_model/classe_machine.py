from odoo import models, fields, api

class ClasseMachine(models.Model):
	_name = 'fleet.vehicle.class'
	_description = "Directeur"
	_inherit = ['mail.thread', 'mail.activity.mixin']
	

	name = fields.Char('Libellé')
	description = fields.Char('Description')

	