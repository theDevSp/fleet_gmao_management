# -*- coding: utf-8 -*-
import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError


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


class fleet_line_reparation(models.Model):
	_name = 'fleet.line.reparation'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char('Description')
	nomenclature_id = fields.Many2one('product.nomenclature', 'Modèle', ondelete='restrict')
	product_id = fields.Many2one('product.product', 'Référence Pièces',
	                             domain="[('nomenclature_id.product_is','=','piece')]",
	                             ondelete='restrict')
	notes = fields.Text('Observation')
	price_unit = fields.Float('Prix unitaire')
	qty = fields.Integer("Quantité")
	uom_id = fields.Many2one('product.uom', 'Unité')
	option = fields.Char("Option")
	log_id = fields.Many2one("fleet.vehicle.log.services", "Service")
	filtre_id = fields.Many2one('fleet.filtre', 'Filtre')
	filtre_template_id = fields.Many2one('fleet.filtre.template', "Template")

	@api.onchange('product_id')
	def onchange_product_id(self):
		self.name = self.product_id.name
		self.uom_id = self.product_id.uom_id.id
		self.price_unit = self.product_id.standard_price


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

	def unlink(self):
		group_long_name = ['gmao.group_product_admin', 'gmao.group_product_manager']
		if not self.env['res.users'].has_group(group_long_name[0]) and not self.env['res.users'].has_group(
				group_long_name[1]):
			raise UserError(
				"Pour supprimer ce document, vous devez appartenir au groupe(Suppression de machines et éléments associés)"
				".Veuillez contacter votre administrateur!")
		return super(fleet_filtre_template, self).unlink()


class fleet_filtre_template_type(models.Model):
	_name = 'fleet.filtre.template.type'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = 'Modèle Révision'

	name = fields.Char('Nom', readonly=True)
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

	def unlink(self):
		group_long_name = ['gmao.group_product_admin', 'gmao.group_product_manager']
		if not self.env['res.users'].has_group(group_long_name[0]) and not self.env['res.users'].has_group(
				group_long_name[1]):
			raise UserError(
				"Pour supprimer ce document, vous devez appartenir au groupe(Suppression de machines et éléments associés)"
				".Veuillez contacter votre administrateur!")
		return super(fleet_filtre_template_type, self).unlink()
