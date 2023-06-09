
import datetime
from odoo import models, fields, api
from odoo.exceptions import  UserError

class FleetVehicle(models.Model):
	_inherit = ['fleet.vehicle']
	_name = 'fleet.vehicle'

	class_id = fields.Many2one('fleet.vehicle.class', 'Type', ondelete="restrict")
	serial_number = fields.Char('Numéro de série', index=True)
	designation_id = fields.Many2one('fleet.vehicle.type', 'Type', ondelete="restrict")
	category_id = fields.Many2one('fleet.vehicle.category', 'Catégorie')
	brand_id = fields.Many2one('fleet.vehicle.brand','Marque')
	model_id = fields.Many2one('fleet.vehicle.model', 'Model',required=False, help='Model of the vehicle')

	location_id = fields.Many2one('stock.location', 'Équipe (Location)')
	capacity = fields.Char('Capacité')
	odometer_unit = fields.Selection([('heures',"Heures"),('kilometers', 'Kilometers')], 'Odometer Unit',required=True)

	emplacement_chantier_id = fields.Many2one('fleet.vehicle.chantier.emplacement', 'Emplacement sur chantier'
					# ,domain=lambda self: [('chantier_ids', '=', self.chantier_id.id)]
				)
	chantier_id = fields.Many2one('fleet.vehicle.chantier', 'Chantier d\'affectation', required=True)
	date_mise_service = fields.Date("Mise en service")
	date_transfert_chantier = fields.Date("Date d'entrée chantier")
	date_debut_garantie = fields.Date("Date Début Garantie")
	date_delivery = fields.Date("Date Livraison")
	date_fin_garantie = fields.Date("Date Fin Garantie")
	garantie = fields.Boolean("Garantie",default=True)
	garantie_etat = fields.Selection([("Valide", "Valide"), ("Expiré", "Expirée")], "État garantie",default="Valide")

	partner_id = fields.Many2one("res.partner", "Fournisseur")

	pas_bouclage = fields.Integer('Pas de Bouclage', readonly=True)
	seuil_bouclage = fields.Integer('Seuil de Bouclage', readonly=True)

	code = fields.Char('Code',required=True)
	notes = fields.Text('Notes')
	contract_number = fields.Char('Numéro Contrat')
	folder = fields.Char('Numéro de dossier')
	annee = fields.Char("Année", default=datetime.date.today())
	mode_reglement = fields.Selection([('autofinancement', 'Autofinancement'), ('leasing', 'Leasing')],
	                                  u"Mode règlement")
	state_breakdown = fields.Selection([('disponible', 'Disponible'),
	                                    ('panne_marche', 'En panne marche'),
	                                    ('panne_arret', 'En panne arret'),
	                                    ('reparation', 'En reparation'),
	                                    ('transfert', 'Transfert'),
	                                    ('vendu', 'Vendu'),
	                                    ('rendu', 'Rendu'),
	                                    ('deteriore', 'Deterioré')], string="Statut panne")
	state = fields.Selection([('reception', "En Stock"), ('livraison', "Mise en route")], u"État du matériel")
	date_acquisition = fields.Date('Date d\'acquisition')
	acquisition_amount = fields.Float('Montant d\'acquisition (HT)')
	taxes_id = fields.Many2one('account.tax', u"TVA")
	montant_tva = fields.Float(u"Montant TVA", compute='_compute_tva', readonly=True)
	montant_total = fields.Float(u"Montant Acquisition (TTC)", compute='_compute_tva', readonly=True)
	doc_ids = fields.One2many("fleet.vehicle.echeance",'vehicle_id',u"")

	numero_moteur = fields.Char("Numéro de série du moteur")
	type_moteur = fields.Many2one('fleet.vehicle.motor.type', u"Type moteur")

	@api.depends('taxes_id')
	def _compute_tva(self):
		self.montant_tva = 0
		self.montant_total = 0
		for machine in self:
			if machine.taxes_id:
				machine.montant_tva = machine.acquisition_amount * machine.taxes_id.amount
				machine.montant_total = machine.acquisition_amount + machine.montant_tva
			else:
				pass

	@api.model
	def create(self, vals):
		res = super(FleetVehicle, self).create(vals)
		if vals.get("code"):
			location_name = res.name + "/" + res.code
			data_location_engine = {
				"name": location_name,
				'usage': 'internal',
			}
			location_id = self.env['stock.location'].create(data_location_engine)
			vals['location_id'] = location_id.id

		return res

	def write(self, vals):
		group_long_name = "gmao.group_product_admin"
		if not self.env['res.users'].has_group(group_long_name):
			raise UserError("Erreur droit d'accès! \n Vous n'êtes pas autorisé à modfier un engin!")
		return super(FleetVehicle, self).write(vals)
