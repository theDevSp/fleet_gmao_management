# -*- coding: utf-8 -*-
import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError


class FleetVehicleModification(models.Model):
	_name = 'fleet.vehicle.modification'

	vehicle_id = fields.Many2one('fleet.vehicle', 'Engin')
	related_vehicle_id = fields.Many2one('fleet.vehicle', 'Engin rattaché')
	date = fields.Date('Date')