
from odoo import models, fields, api
import datetime
from dateutil.relativedelta import relativedelta

class FleetVehicleEcheance(models.Model):
	_name = 'fleet.vehicle.echeance'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	vehicle_id = fields.Many2one('fleet.vehicle', 'Engin', required=True)
	document_id = fields.Many2one('fleet.vehicle.administratif.documents','Document',required=True)
	date_start = fields.Date('Date Début',required=True)
	date_end = fields.Date('Date Fin',required=True)

	@api.onchange("date_start", "document_id", "date_start")
	def onchange_action_liquide(self):
		if self.document_id and self.date_start:
			if self.document_id.period_dmy == 'd':
				self.date_end = (datetime.datetime.strptime(self.date_start, '%Y-%m-%d') + relativedelta(
					days=+ self.document_id.period_count))
			elif self.document_id.period_dmy == 'm':
				self.date_end = (datetime.datetime.strptime(self.date_start, '%Y-%m-%d') + relativedelta(
					months=+ self.document_id.period_count))
			else:
				self.date_end = (datetime.datetime.strptime(str(self.date_start), '%Y-%m-%d') + relativedelta(
					years=+ self.document_id.period_count))

