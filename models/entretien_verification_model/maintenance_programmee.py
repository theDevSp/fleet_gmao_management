# -*- coding: utf-8 -*-

from datetime import date, timedelta, datetime
from math import ceil
from lxml import etree
from odoo import models, fields, api
from odoo.exceptions import ValidationError


STATE_SELECTION = [
        ('draft', 'Brouillon'),
        ('confirm', 'Confirmée'),
        ('done', 'Effectuée'),
        ('cancel', 'Annuler')
    ]
STATE2_SELECTION = [
        ('in_progress',"En cours"), #couleur verte   qd client confirme intervention
        ('warning', 'Délai proche'),#couleur orange qd on est dans le delai préciser par le paramètre
        ('error', 'Dépassé'),#couleur rouge  après delai
        ('confirm', 'confirmée'),
        ('done', 'Effectuée'),#couleur noir qd effectuer
        ('cancel', 'Annuler'),
    ]
class fleet_vehicle_pm(models.Model):
    _name = "fleet.vehicle.pm"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Maintenance preventive"
    _order="vehicle_id asc"

    def unlink(self):
        for prog in self:
            if prog.state not in ('draft', 'cancel'):
                raise ValidationError("Erreur, Vous ne pouvez pas supprimer une maintenance programmée, songez à l\'annuler.")
        return super(fleet_vehicle_pm, self).unlink()
      
    name = fields.Char(string='Réf MP')
    state = fields.Selection(STATE_SELECTION,string='Etat',default='draft',tracking=True)
    state_two = fields.Selection(STATE2_SELECTION, string='Statut', compute='_compute_state_two',store=True)

    line_ids = fields.One2many("fleet.line.reparation","pm_id",string="Pièces de rechange")
    checklist_ids1 = fields.One2many('fleet.line.checklist','pm_id',string='Niveau',domain=[('name.code', '=', 'niveau')])
    checklist_ids2 = fields.One2many('fleet.line.checklist','pm_id',string='Graissage',domain=[('name.code', '=', 'graissage')])
    checklist_ids3 = fields.One2many('fleet.line.checklist','pm_id',string='Pression',domain=[('name.code', '=', 'pression')])
    checklist_ids4 = fields.One2many('fleet.line.checklist','pm_id',string='Remplacement huile',domain=[('name.code', '=', 'huile')])
    checklist_ids5 = fields.One2many('fleet.line.checklist','pm_id',string='Autre entretien',domain=[('name.code', '=', 'autres')])
    vidange = fields.Boolean(string="Sans Vidange")
    plan = fields.Integer(string='Plan appliqué',help="Cette valeur indique le plan d'entretien appliqué")
    date_start = fields.Datetime(string="Date Reception")
    date_end = fields.Datetime(string="Date fin")
    date = fields.Date(string="Date prévue",default=fields.Date.context_today)
    type_id =fields.Many2one("fleet.filtre.template.type",string="Type")
    chantier_id =fields.Many2one('fleet.vehicle.chantier', string='Chantier',required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Engin',required=True)
    description = fields.Text('Description')
    maintenance_type = fields.Selection([('pm','Mainteance programmée')],string='Type')
    employee_id = fields.Many2one("hr.employee",string="Employé")

    # @api.model
    # def create(self, vals):
    #     vals['name'] = self.env['ir.sequence'].get('fleet.vehicle.pm')
    #     return 

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        picking = self.create_stock_picking()
        self.state = 'done'
        self.picking_id = picking.id

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

        
    