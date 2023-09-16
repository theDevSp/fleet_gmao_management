# -*- coding: utf-8 -*-

from odoo import models, fields, api

class fleet_filtre(models.Model):
	_name = 'fleet.filtre'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Integer('Révision', required=True)

	reparation_ids = fields.One2many("fleet.line.reparation", "filtre_id", "Remplacement pieces")

	checklist_ids1 = fields.One2many('fleet.line.checklist', 'filtre_id', 'Niveau',
	                                 domain=[('name.code', '=', 'niveau')])
	checklist_ids2 = fields.One2many('fleet.line.checklist', 'filtre_id', 'Graissage',
	                                 domain=[('name.code', '=', 'graissage')])
	checklist_ids3 = fields.One2many('fleet.line.checklist', 'filtre_id', 'Pression',
	                                 domain=[('name.code', '=', 'pression')])
	checklist_ids4 = fields.One2many('fleet.line.checklist', 'filtre_id', 'Remplacement huile',
	                                 domain=[('name.code', '=', 'huile')])
	checklist_ids5 = fields.One2many('fleet.line.checklist', 'filtre_id', 'Autres entretiens',
	                                 domain=[('name.code', '=', 'autres')])
	
	vehicle_id = fields.Many2one("fleet.vehicle", "Machine", required=True, ondelete="restrict")
	active = fields.Boolean('Active', default=True)
	type_id = fields.Many2one("fleet.filtre.template.type", "Type")

	def copy(self, default=None):

		default = dict(default or {})
		rep_line_ids = []
		result = super(fleet_filtre, self).copy(default=default)
		for filter in self:
			for line in filter.reparation_ids:
				rep_id = self.env['fleet.line.reparation'].create({'product_id': line.product_id.id,
				                                                   'name': line.product_id.name,
				                                                   'qty': line.qty})

				rep_line_ids.append(rep_id.id)
			for line in filter.checklist_ids1:
				check_id = self.env['fleet.line.checklist'].create({'name': line.name.id})
				for ch_id in check_id:
					ch_id.write({'filtre_id': result})
			for line in filter.checklist_ids2:
				check_id = self.env['fleet.line.checklist'].create({'name': line.name.id})
				for ch_id in check_id:
					self.env['fleet.line.checklist'].browse(ch_id.id).write({'filtre_id': result})
			for line in filter.checklist_ids3:
				check_id = self.env['fleet.line.checklist'].create({'name': line.name.id})
				for ch_id in check_id:
					self.env['fleet.line.checklist'].browse(ch_id.id).write({'filtre_id': result})
			for line in filter.checklist_ids4:
				check_id = self.env['fleet.line.checklist'].create({'name': line.name.id})
				for ch_id in check_id:
					self.env['fleet.line.checklist'].browse(ch_id.id).write({'filtre_id': result})
			for line in filter.checklist_ids5:
				check_id = self.env['fleet.line.checklist'].create({'name': line.name.id})
				self.env['fleet.line.checklist'].write({'filtre_id': result})
		self.env['fleet.line.reparation'].browse(rep_line_ids).write({'filtre_id': result})
		return result