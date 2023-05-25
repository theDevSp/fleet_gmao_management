# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError


class product_template_type(models.Model):
	_name = 'product.template.type'

	name = fields.Char('Nom Type', size=64)



class product_brand(models.Model):
	_name = "product.brand"

	name = fields.Char("Nom Modèle", required=True)
	code = fields.Char("Code Modèle")

