from odoo import models, fields, api

class fleet_verification_type(models.Model):
	_name = 'fleet.verification.type'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char('Nom', required=True)
	code = fields.Integer("Code")