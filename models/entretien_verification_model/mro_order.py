from odoo import models,fields,api
from odoo.exceptions import ValidationError


class mro_order(models.Model):
    _name = 'mro.order'

    MAINTENANCE_TYPE_SELECTION = [
        ('bm', 'Breakdown'),
        ('cm', 'Corrective'),
    ]

    maintenance_type = fields.Selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True, readonly=True, states={'draft': [('readonly', False)]})
    vehicle_id = fields.Many2one('fleet.vehicle', 'Engin',required=True)
    chantier_id = fields.Many2one('fleet.vehicle.chantier', 'Chantier',required=True)
    service_type_id = fields.Many2one('fleet.intervention.zone', "Catégorie de maintenance")
    employee_id = fields.Many2one('hr.employee', "Chef de matériel") # a remplacer par responsable
    date_start = fields.Date('Date début de panne')
    date_end = fields.Date('Date fin de panne')
    duree_saisie = fields.Float('Durée saisie')# compute depends de date_start et date_end
    description = fields.Char('Type de panne',required=True,size=1000)
    odometer = fields.Float('Compteur')
    type_id = fields.Many2one('fleet.filtre.template.type','Type de template')


    def _check_date_end(self,cr,uid,ids,context=None):
        for rec in self.browse(cr,uid,ids,context=context):
            if not rec.date_end:
                raise ValidationError(
                    "Erreur, Vous devez préciser la date de fin de panne pour clôturer."
                )   
            if rec.date_end < rec.date_start:
                raise ValidationError(
                    "Erreur, Date début <= Date fin."
                )

    def unlink(self, cr, uid, ids, context=None):
        for mro in self.browse(cr,uid,ids):
            if mro.state in ('ready','done'):
                raise ValidationError("Erreur, Vous devez d'abord annuler.")
        return super(mro_order,self).unlink(cr,uid,ids,context=context)
    

    @api.onchange('chantier_id')
    def onchange_chantier_id(self):
        if self.chantier_id:
            self.zone_id = self.chantier_id.zone_id.id
            
    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        if self.vehicle_id:
            self.vehicle_state = self.vehicle_id.state_breakdown
            self.employee_id = self.vehicle_id.chantier_employee_id.id
            self.chantier_id = self.vehicle_id.chantier_id.id
            self.odometer = self.vehicle_id.compteur
        else:
            self.employee_id = False
            self.chantier_id = False   
            self.vehicle_state = False


    def action_confirm(self, cr, uid, ids, context=None):
        for mro in self.browse(cr,uid,ids):
            mro.vehicle_id.state_breakdown = mro.vehicle_state  
        return super(mro_order,self).action_confirm(cr, uid, ids, context=context)  
    
    def action_ready(self, cr, uid, ids):
        for mro in self.browse(cr,uid,ids):
            mro.vehicle_id.state_breakdown = mro.vehicle_state
        return super(mro_order,self).action_ready(cr, uid, ids) 

    def action_done(self, cr, uid, ids, context=None):
        dispo_vehicle_ids = []
        self._check_date_end(cr,uid,ids,context=context)
        for mro in self.browse(cr,uid,ids):
            if mro.vehicle_state in ('panne_arret','panne_marche','reparation'):
                dispo_vehicle_ids.append(mro.vehicle_id.id)
        self.env['fleet.vehicle'].write(cr,uid,dispo_vehicle_ids,{'state_breakdown':'disponible'})
        return super(mro_order,self).action_done(cr, uid, ids, context=context)

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.env['ir.sequence'].next_by_code('mro.order') or '/'
        return super(mro_order, self).create(cr, uid, vals, context=context)

    def write(self,cr,uid,ids,vals,context=None):
        vehicle_ids = []
        result =super(mro_order,self).write(cr,uid,ids,vals,context=context)
        if 'vehicle_state' in vals:
            for mro in self.browse(cr,uid,ids):
                if mro.state not in ('draft','done'):
                    vehicle_ids.append(mro.vehicle_id.id)
            self.env['fleet.vehicle'].write(cr,uid,vehicle_ids,{'state_breakdown':vals.get('vehicle_state')})
        return result