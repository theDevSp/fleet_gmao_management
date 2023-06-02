# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api

class fleet_line_reparation(models.Model):
	_name = 'fleet.line.reparation'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char('Description')
	product_id = fields.Many2one('product.product', 'Référence Pièces',
	                             ondelete='restrict')
	notes = fields.Text('Observation')
	price_unit = fields.Float('Prix unitaire')
	qty = fields.Integer("Quantité")
	uom_id = fields.Many2one('product.uom', 'Unité')
	option = fields.Char("Option")
	log_id = fields.Many2one("fleet.vehicle.log.services", "Service")
	filtre_id = fields.Many2one('fleet.filtre', 'Filtre')
	filtre_template_id = fields.Many2one('fleet.filtre.template', "Template")
	pm_id = fields.Many2one('fleet.vehicle.pm',"Maintenance programmé")

	@api.onchange('product_id')
	def onchange_product_id(self):
		self.name = self.product_id.name
		self.uom_id = self.product_id.uom_id.id
		self.price_unit = self.product_id.standard_price