# -*- coding: utf-8 -*-

from odoo import models,fields

class fleet_intervention_catgory(models.Model):
    _name='fleet.intervention.zone'
    _description = "Fleet Intervention Zone"
    _inherit = ['mail.thread','mail.activity.mixin']
   
    name = fields.Char("Nom de la catégorie",required=True)


