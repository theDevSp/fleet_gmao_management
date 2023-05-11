# -*- coding: utf-8 -*-
import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from calendar import monthrange
from odoo.exceptions import AccessError, UserError, ValidationError


class fleet_vehicle_activity(models.Model):
	_name = "fleet.vehicle.activity"
	_description = 'Activités Machine'

	def _get_cost(self):
		for rec in self:
			if rec.period_id and rec.days:
				days_of_current_month = monthrange(rec.period_id.date_start.year, rec.period_id.date_start.month)[1]
				rec.montant_jour = rec.montant_location / days_of_current_month
				rec.montant_total = rec.montant_jour * rec.days

	@api.onchange('period_id')
	def _onchange_period_id(self):
		self._get_cost()

	@api.onchange('days')
	def _onchange_days(self):
		self._get_cost()

	@api.onchange('montant_location')
	def _onchange_montant_location(self):
		self._get_cost()

	date = fields.Date('Date', required=True)
	period_id = fields.Many2one('account.month.period', 'Mois', required=True)
	days = fields.Float('Nombre de jours  actifs')
	notes = fields.Text('Notes')
	vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicule', required=True)
	montant_location = fields.Float('Montant location')
	montant_jour = fields.Float('Côut Journalier')
	montant_total = fields.Float('Côut Mensuelle')

