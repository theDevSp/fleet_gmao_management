# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError


class product_vehicle(models.Model):
	_inherit = ['product.product']
	_name = 'product.product'

	affectation_ids = fields.One2many('product.template.affectation', related='product_tmpl_id.affectation_ids',
	                                  string='Affectations')
	related_product_ids = fields.Many2many('product.product', 'product_product_product_product_relation', 'product_id1',
	                                       'product_id2', string="Equivalents")


class product_template(models.Model):
	_inherit = ['product.template']
	_name = 'product.template'

	affectation_ids = fields.One2many('product.template.affectation', 'product_tmpl_id', 'Affectations')
	related_product_ids = fields.Many2many(related='product_variant_ids.related_product_ids', string="Equivalents")
	nomenclature_id = fields.Many2one('product.nomenclature', 'Modele', ondelete="restrict")

	@api.model
	def create(self, vals):
		allowed_groups = [
			'fleet_gmao_management.group_product_admin',
			'fleet_gmao_management.group_product_manager'
		]

		if not self.env.user.has_group(allowed_groups[0]) and not self.env.user.has_group(allowed_groups[1]):
			raise AccessError('Vous n\'êtes pas autorisé à créer un article!')
		if not vals.get('nomenclature_id'):
			group_id = self.env['product.nomenclature'].search([('name', '=', vals.get('name'))])
			if group_id:
				vals['nomenclature_id'] = group_id[0]
			else:
				group_id = self.env['product.nomenclature'].create({'name': vals.get('name')})
				vals['nomenclature_id'] = group_id.id
		return super(product_template, self).create(vals)

	def write(self, vals, context=None):
		allowed_groups = [
			'fleet_gmao_management.group_product_admin',
			'fleet_gmao_management.group_product_manager'
		]
		if not self.env.user.has_group(allowed_groups[0]) and not self.env.user.has_group(allowed_groups[1]):
			raise AccessError('Vous n\'êtes pas autorisé à modifier un article!')
		return super(product_template, self).write(vals, context=context)

	def unlink(self, vals, context=None):
		allowed_groups = 'fleet_gmao_management.group_product_admin'
		if not self.env.user.has_group(allowed_groups):
			raise AccessError('Vous n\'êtes pas autorisé à supprimer un article!')
		return super(product_template, self).write(vals, context=context)


class product_template_type(models.Model):
	_name = 'product.template.type'

	name = fields.Char('Nom Type', size=64)


class product_nomenclature(models.Model):
	_name = "product.nomenclature"

	name = fields.Char("Modèle", required=True)
	product_is = fields.Selection([('MP', 'Matiére Première'), ('Accessoire', 'Accessoire'),
	                               ('Fournitures/Bureautique', 'Fournitures et Bureautique'), ('machine', 'Machine'),
	                               ('piece', 'Pièce')], 'Est ?')

	_sql_constraints = [
		('name_uniq', 'unique(name)', 'Le nom du modèle doit être unique.'),
	]


class product_brand(models.Model):
	_name = "product.brand"

	name = fields.Char("Nom Modèle", required=True)
	code = fields.Char("Code Modèle")


class product_template_affectation(models.Model):
	_name = "product.template.affectation"

	type_id = fields.Many2one('product.template.type', 'Type', ondelete="restrict")
	nomenclature_id = fields.Many2one('product.nomenclature', 'Désignation')
	product_tmpl_id = fields.Many2one('product.template', 'Article')
	vehicle_id = fields.Many2one('fleet.vehicle', 'Machine', ondelete="restrict")

	@api.onchange('vehicle_id')
	def onchange_vehicle_id(self):
		if self.vehicle_id:
			self.type_id = self.vehicle_id.designation_id.id
			self.nomenclature_id = self.vehicle_id.product_id.nomenclature_id.id
