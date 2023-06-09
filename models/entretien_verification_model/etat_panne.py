from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import datetime

class mro_order(models.Model):
    _name = 'mro.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    MAINTENANCE_TYPE_SELECTION = [
        ('bm', 'Breakdown'),
        ('cm', 'Corrective'),
    ]

    name = fields.Char("Réf", default="New")
    maintenance_type = fields.Selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True
                                        # ,readonly=True, states={'draft': [('readonly', False)]}
                                        )
    vehicle_id = fields.Many2one('fleet.vehicle', 'Engin',required=True)
    chantier_id = fields.Many2one('fleet.vehicle.chantier', 'Chantier',required=True)
    service_type_id = fields.Many2one('fleet.intervention.zone', "Catégorie de maintenance")
    employee_id = fields.Many2one('hr.responsable.chantier', "Chef de matériel")
    date_start = fields.Date('Date début de panne')
    date_end = fields.Date('Date fin de panne')
    duree_saisie = fields.Float('Durée saisie')
    description = fields.Char('Type de panne',required=True,size=1000)
    odometer = fields.Float('Compteur')
    type_id = fields.Many2one('fleet.filtre.template.type','Type de template')
    vehicle_state = fields.Selection([('disponible', 'Disponible'),
	                                    ('panne_marche', 'En panne marche'),
	                                    ('panne_arret', 'En panne arret'),
	                                    ('reparation', 'En reparation'),
	                                    ('transfert', 'Transfert'),
	                                    ('vendu', 'Vendu'),
	                                    ('rendu', 'Rendu'),
	                                    ('deteriore', 'Deterioré')], string="Statut panne")
    
    state = fields.Selection([('draft', "Brouillon"), ('ready', "Prêt"), ('cancel', "Annulé"), ('done', "Terminé")], default="draft", string=u"État du matériel")


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
    

    # @api.onchange('chantier_id')
    # def onchange_chantier_id(self):
    #     if self.chantier_id:
    #         self.zone_id = self.chantier_id.zone_id.id
            
    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        if self.vehicle_id:
            self.vehicle_state = self.vehicle_id.state_breakdown
            self.employee_id = self.vehicle_id.driver_id.id
            self.chantier_id = self.vehicle_id.chantier_id.id
            self.odometer = self.vehicle_id.odometer
        else:
            self.employee_id = False
            self.chantier_id = False   
            self.vehicle_state = False

    def to_draft(self):
        if self.state not in {'draft'} :
            self.state = 'draft'
        else:
            raise ValidationError(
                    "Erreur, Cette action n'est pas autorisée."
                )

    def to_ready(self):
        if self.state not in {'ready'} :
            self.state = 'ready'
        else:
            raise ValidationError(
                    "Erreur, Cette action n'est pas autorisée."
                )
        
    def to_annulee(self):
        if self.state not in {'cancel'} :
            self.state = 'cancel'
        else:
            raise ValidationError(
                    "Erreur, Cette action n'est pas autorisée."
                )
    
    def to_terminee(self):
        if self.state not in {'draft','done'} :
            self.state = 'done'
        else:
            raise ValidationError(
                    "Erreur, Cette action n'est pas autorisée."
                )
 

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mro.order.sequence') or 'New'
        return super(mro_order, self).create(vals)


    def write(self,vals):
        result = super(mro_order, self).write(vals)
        return result