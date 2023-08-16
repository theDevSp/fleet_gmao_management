from odoo import models, fields, api

class fleet_filtre_template_type(models.Model):
	_name = 'fleet.filtre.template.type'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = 'Modèle Révision'

	name = fields.Char('Nom', readonly=True, required = True)
	pas_bouclage = fields.Integer("Pas de bouclage", required=True)
	seuil_bouclage = fields.Integer("Seuil de bouclage", required=True)
	sans_suivi = fields.Boolean('Machines sans révision')

	@api.model
	def create(self, vals):
		vals['name'] = str(vals['pas_bouclage']) + '/' + str(vals['seuil_bouclage'])
		return super(fleet_filtre_template_type, self).create(vals)


	def write(self, vals):
		res = super(fleet_filtre_template_type, self).write(vals)
		if 'pas_bouclage' in vals or 'seuil_bouclage' in vals:
			self.name = str(self.pas_bouclage) + '/' + str(self.seuil_bouclage)
		return res
