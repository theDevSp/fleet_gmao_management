from odoo import models, fields

class fleet_filtre_template(models.Model):
	_name = 'fleet.filtre.template'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Integer('Révision', required=True)

	reparation_ids = fields.One2many("fleet.line.reparation", "filtre_template_id", "Reparations")

	checklist_ids1 = fields.One2many('fleet.line.checklist', 'filtre_template_id', 'Niveau',
	                                 domain=[('name.code', '=', 'niveau')])
	checklist_ids2 = fields.One2many('fleet.line.checklist', 'filtre_template_id', 'Graissage',
	                                 domain=[('name.code', '=', 'graissage')])
	checklist_ids3 = fields.One2many('fleet.line.checklist', 'filtre_template_id', 'Pression',
	                                 domain=[('name.code', '=', 'pression')])
	checklist_ids4 = fields.One2many('fleet.line.checklist', 'filtre_template_id', 'Remplacement huile',
	                                 domain=[('name.code', '=', 'huile')])
	checklist_ids5 = fields.One2many('fleet.line.checklist', 'filtre_template_id', 'Autre entretien',
	                                 domain=[('name.code', '=', 'autres')])
	designation_id = fields.Many2one("product.template.type", "Type de machine", required=True,
	                                 ondelete='restrict')
	
	type_id = fields.Many2one("fleet.filtre.template.type", "Type")

	def copy(self, default=None):
		default = dict(default or {})
		rep_line_ids = []
		result = super(fleet_filtre_template, self).copy(default=default)
		for template in self:
			for line in template.reparation_ids:
				rep_id = self.env['fleet.line.reparation'].create({'nomenclature_id': line.nomenclature_id.id,
				                                                   'name': line.nomenclature_id.name,
				                                                   'qty': line.qty})
				rep_line_ids.append(rep_id.id)
			for line in template.checklist_ids1:
				check_id = self.env['fleet.line.checklist'].create({'name': line.name.id})
				for ch_id in check_id:
					self.env['fleet.line.checklist'].browse(ch_id.id).write({'filtre_template_id': result})
			for line in template.checklist_ids2:
				check_id = self.env['fleet.line.checklist'].create({'name': line.name.id})
				for ch_id in check_id:
					self.env['fleet.line.checklist'].browse(ch_id.id).write({'filtre_template_id': result})
			for line in template.checklist_ids3:
				check_id = self.env['fleet.line.checklist'].create({'name': line.name.id})
				for ch_id in check_id:
					self.env['fleet.line.checklist'].browse(ch_id.id).write({'filtre_template_id': result})
			for line in template.checklist_ids4:
				check_id = self.env['fleet.line.checklist'].create({'name': line.name.id})
				for ch_id in check_id:
					self.env['fleet.line.checklist'].browse(ch_id.id).write({'filtre_template_id': result})
			for line in template.checklist_ids5:
				check_id = self.env['fleet.line.checklist'].create({'name': line.name.id})
				for ch_id in check_id:
					self.env['fleet.line.checklist'].browse(ch_id.id).write({'filtre_template_id': result})
		self.env['fleet.line.reparation'].write(rep_line_ids, {'filtre_template_id': result})
		return result
