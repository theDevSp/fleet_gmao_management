# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields

class fleet_line_checklist(models.Model):
	_name = 'fleet.line.checklist'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Many2one('fleet.verification', 'Vérification')
	fait = fields.Boolean("Ajouter")
	log_id = fields.Many2one("fleet.vehicle.log.services", "Service")
	filtre_id = fields.Many2one('fleet.filtre', "Filtre")
	filtre_template_id = fields.Many2one('fleet.filtre.template', "Template")
	pm_id = fields.Many2one('fleet.vehicle.pm',"Maintenance programmé")

	_sql_constraints = [
		('name_filtre_id_uniq', 'unique(name,filtre_id)', 'Cette vérification existe déjà !'),
		('name_filtre_template_id_uniq', 'unique(name,filtre_template_id)', 'Cette vérification existe déjà !')
	]