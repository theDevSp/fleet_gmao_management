# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class fleet_vehicle_chantier_affectation(models.Model):
    _name = "fleet.vehicle.chantier.affectation"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Ref',readonly=True, default="New")
    vehicle_id = fields.Many2one('fleet.vehicle','Machine',ondelete="restrict",required=True,readonly=True, states={'draft': [('readonly', False)]})
    vehicle_chantier_id = fields.Many2one('fleet.vehicle.chantier','Chantier de départ',ondelete="restrict",readonly=True, states={'draft': [('readonly', False)]})
    chantier_id = fields.Many2one('fleet.vehicle.chantier',"Chantier d'arrivé",ondelete="restrict",required=True,readonly=True, states={'draft': [('readonly', False)]})
    date_start = fields.Date("Date de transfert",default=date.today(),required=True,readonly=True, states={'draft': [('readonly', False)]})
    date_end = fields.Date("Date de fin")
    state = fields.Selection([('draft','En saisie'),('done','Confirmé')],'Statut',default='draft')

    # product_id = fields.Many2one('product.product',string='Désignation',related="vehicle_id.product_id",store=True,readonly=True)

    capacity = fields.Char(string='Capacité',
                                 related="vehicle_id.capacity",store=True,readonly=True)

    brand_id = fields.Many2one('fleet.vehicle.brand',string='Marque',
                                 related="vehicle_id.brand_id",store=True,readonly=True)

    type = fields.Many2one(string='Type',related="vehicle_id.designation_id",store=True,readonly=True)
    
    emplacement_source_id = fields.Many2one('fleet.vehicle.chantier.emplacement','Équipe de départ',ondelete="restrict",readonly=True, states={'draft': [('readonly', False)]})
    emplacement_chantier_id = fields.Many2one('fleet.vehicle.chantier.emplacement',"Équipe d'arrivé",ondelete="restrict",readonly=True, states={'draft': [('readonly', False)]})
    notes = fields.Text('Observation')

    @api.model
    @api.returns('self', lambda value:value.id)
    def create(self, vals):
        vehicle =  self.env['fleet.vehicle'].browse(vals.get('vehicle_id'))
        if vehicle.chantier_id:
            if vals.get('vehicle_chantier_id') != vehicle.chantier_id.id:
                raise ValidationError(
                    "Erreur, Le chantier de départ ne correspond pas au chantier qui est sur la fiche de l'engin."
                )
        if ('name' not in vals) or (vals.get('name') == '/'):
            vals['name'] =  self.env['ir.sequence'].next_by_code('fleet.vehicle.chantier.affectation.sequence')

        aff_id = super(fleet_vehicle_chantier_affectation, self).create(vals)
        print(aff_id)
        #self.set_vehcile_chantier(cr,uid,[aff_id],vals.get('vehicle_id'),vals.get('chantier_id'),vals.get('date_start'))
        return aff_id

    def write(self, vals):
        print(self.env.context)
        if not self.env.context.get('no_warning'):
            if self.vehicle_id.chantier_id:
                if 'vehicle_chantier_id' in vals:
                    print(self.vehicle_id.chantier_id.name)
                    if vals.get('vehicle_chantier_id') != self.vehicle_id.chantier_id.id:
                        raise ValidationError(
                            "Erreur, Le chantier de départ ne correspond pas au chantier qui est sur la fiche de l'engin."
                        )
                else:
                    if self.vehicle_chantier_id.id != self.vehicle_id.chantier_id.id:
                        raise ValidationError(
                            "Erreur, Le chantier de départ ne correspond pas au chantier qui est sur la fiche de l'engin."
                        )
        return models.Model.write(self, vals)

    @api.onchange('chantier_id')
    def onchange_chantier_id(self):
        self.emplacement_chantier_id = False

    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        self.vehicle_chantier_id = self.vehicle_id.chantier_id.id  
        self.emplacement_source_id = self.vehicle_id.emplacement_chantier_id.id  

    @api.onchange('vehicle_chantier_id')
    def onchange_vehicle_chantier_id(self):
        if self.vehicle_id.chantier_id.id and self.vehicle_chantier_id.id:
            if self.vehicle_chantier_id.id != self.vehicle_id.chantier_id.id:
                raise ValidationError(
                    "Erreur, Le chantier de départ ne correspond pas au chantier qui est sur la fiche de l'engin."
                )

    @api.onchange('emplacement_source_id')
    def onchange_emplacement_source_id(self):
        if self.vehicle_id.emplacement_chantier_id.id and self.emplacement_source_id.id:
            if self.emplacement_source_id.id != self.vehicle_id.emplacement_chantier_id.id:
                raise ValidationError("Erreur, L'emplacement de départ ne correspond pas à celui  qui est sur la fiche de l'engin.")
    
    def action_done(self,cr,uid,ids,context=None):
        data = self.browse(cr,uid,ids[0])
        self.set_vehcile_chantier(cr,uid,ids,data.vehicle_id.id,data.chantier_id.id,data.emplacement_source_id.id,data.emplacement_chantier_id.id,data.date_start,context={"no_warning":True})
        return True

    def action_draft(self,cr,uid,ids,context=None):
        data = self.browse(cr,uid,ids[0])
        res_ids = self.search(cr,uid,[('vehicle_id','=',data.vehicle_id.id)],order="id desc")
        if res_ids[0] != ids[0]: ##
            raise ValidationError("Erreur! Cette option n'est disponible que sur le dernier transfert")
        self.write(cr,uid,ids[0],{'state':'draft'},context={"no_warning":True})
        self.unset_vehcile_chantier(cr,uid,ids,data.vehicle_id.id,data.vehicle_chantier_id.id,data.emplacement_source_id.id)
        return True
    
    def copy(self, cr, uid, res_id, default=None, context={}):
        if default is None:
            default = {}
        default = default.copy()
        default['name'] =  self.env['ir.sequence'].next_by_code('fleet.vehicle.chantier.affectation.sequence')
        default['state'] = 'draft'
        return super(fleet_vehicle_chantier_affectation, self).copy(cr, uid, res_id, default, context)
    
    def unlink(self, cr, uid, ids, context=None):
        for aff in self.browse(cr,uid,ids):
            if aff.state == 'done':
                raise ValidationError("Suppression impossible! Vous ne pouvez pas supprimer une affectation déjà traitée.")
        return super(fleet_vehicle_chantier_affectation, self).unlink(cr, uid, ids, context)   

    def set_vehcile_chantier(self, cr, uid, ids,vehicle_id,chantie_id,emplacement_source_id,emplacement_chantier_id,date_start, context={}):
        vehicle = self.env['fleet.vehicle'].browse(cr,uid,vehicle_id)
        old_chantier_id = vehicle.chantier_id.id
        old_histo_id = self.search(cr,uid,[('state','=','done'),('vehicle_id','=',vehicle_id),('chantier_id','=',old_chantier_id)])
        
        chantier = self.pool['fleet.vehicle.chantier'].browse(cr,uid,chantie_id)
        self.env['fleet.vehicle'].write(cr,uid,vehicle_id,{'date_transfert':date_start,'chantier_employee_id':chantier.chantier_employee_id.id,'chantier_id':chantie_id,'emplacement_chantier_id':emplacement_chantier_id})
        self.write(cr,uid,ids,{'state':'done'},context)
        self.write(cr,uid,old_histo_id,{'date_end':date_start},context)
        return True

    def unset_vehcile_chantier(self, cr, uid, ids,vehicle_id,vehicle_chantie_id,emplacement_source_id,context={}):
        chantier = self.env['fleet.vehicle.chantier'].browse(cr,uid,vehicle_chantie_id)
        self.env['fleet.vehicle'].write(cr,uid,vehicle_id,{'chantier_employee_id':chantier.chantier_employee_id.id,'chantier_id':vehicle_chantie_id,'emplacement_chantier_id':emplacement_source_id})
        return True