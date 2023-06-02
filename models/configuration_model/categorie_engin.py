# -*- coding: utf-8 -*-
import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError

class FleetVehicleCategory(models.Model):
	_name = 'fleet.vehicle.category'

	name = fields.Char('Nom', required=True)
	note = fields.Text('Description')
