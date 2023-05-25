# -*- coding: utf-8 -*-
import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError


class fleet_line_checklist(models.Model):
	_name = 'fleet.line.checklist'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Many2one('fleet.verification', 'Vérification')
	fait = fields.Boolean("Ajouter")
	log_id = fields.Many2one("fleet.vehicle.log.services", "Service")
	filtre_id = fields.Many2one('fleet.filtre', "Filtre")
	filtre_template_id = fields.Many2one('fleet.filtre.template', "Template")

	_sql_constraints = [
		('name_filtre_id_uniq', 'unique(name,filtre_id)', 'Cette vérification existe déjà !'),
		('name_filtre_template_id_uniq', 'unique(name,filtre_template_id)', 'Cette vérification existe déjà !')
	]


class fleet_verification(models.Model):
	_name = 'fleet.verification'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char('Nom de la vérification')
	code = fields.Selection([('niveau', 'Niveau'), ('graissage', 'Graissage'), ('pression', 'Pression'),
	                         ('huile', 'Remplacement huile'), ('autres', 'Autres entretiens')], "Code")

class fleet_verification_type(models.Model):
	_name = 'fleet.verification.type'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char('Nom')
	code = fields.Integer("Code")

