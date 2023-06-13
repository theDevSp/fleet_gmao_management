from odoo import models, fields

class fleet_verification(models.Model):
	_name = 'fleet.verification'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char('Nom de la vérification')
	code = fields.Selection([('niveau', 'Niveau'), ('graissage', 'Graissage'), ('pression', 'Pression'),
	                         ('huile', 'Remplacement huile'), ('autres', 'Autres entretiens')], "Code")