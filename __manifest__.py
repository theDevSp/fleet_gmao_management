# -*- coding: utf-8 -*-
{
    'name': "fleet_gmao_management",
    'summary': """Les véhicules""",
    'description': """Déscription des véhicules""",
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base', 'account_fiscal_year_period', 'fleet','construction_site_management','sale', 'purchase', 'stock', 'mail', 'uom',],

    'data': [
		'security/security_groups.xml',
		'security/ir.model.access.csv',
        'views/sequences/pm_sequence.xml',

        # configuration views
        'views/configuration_model/accrochage_view.xml',
        'views/configuration_model/categorie_engin_view.xml',
        'views/configuration_model/type_verification_view.xml',
        'views/configuration_model/type_machine_view.xml',
        'views/configuration_model/marque_view.xml',
        'views/configuration_model/classe_machine_view.xml',
        'views/configuration_model/type_moteur_view.xml',
        
        # document views
        'views/document_model/document_view.xml',
        'views/document_model/echeance_view.xml',

        # entretien et verification views
        'views/entretien_verification_model/tableau_entretien__view.xml',
        'views/entretien_verification_model/tableau_entretien_template_view.xml',
        'views/entretien_verification_model/modele_revision_view.xml',
        'views/entretien_verification_model/verification_view.xml',
        'views/entretien_verification_model/maintenance_programmee_view.xml',
        'views/entretien_verification_model/etat_panne_view.xml',
        
        # machine views
        'views/machine_model/machines_view.xml',
        'views/machine_model/affectation_view.xml',

        # configuration menu
        'views/configuration_model/configuration_menu.xml',
        'views/configuration_model/accrochage_menu.xml',
        'views/configuration_model/categorie_engin_menu.xml',
        'views/configuration_model/type_verification_menu.xml',
        'views/configuration_model/type_machine_menu.xml',
        'views/configuration_model/marque_menu.xml',
        'views/configuration_model/classe_machine_menu.xml',
        'views/configuration_model/type_moteur_menu.xml',
        
        # document menu
        'views/document_model/document_menu.xml',
        'views/document_model/echeance_menu.xml',

        # entretien et verification menu
        'views/entretien_verification_model/entretien_verification_menu.xml',
        'views/entretien_verification_model/tableau_entretien__menu.xml',
        'views/entretien_verification_model/tableau_entretien_template_menu.xml',
        'views/entretien_verification_model/modele_revision_menu.xml',
        'views/entretien_verification_model/verification_menu.xml',
        'views/entretien_verification_model/maintenance_programmee_menu.xml',
        'views/entretien_verification_model/etat_panne_menu.xml',
        
        # machine menu
        'views/machine_model/machines_menu_principal.xml',
        'views/machine_model/machines_menu.xml',
        'views/machine_model/affectation_menu.xml',
	],
    'installable': True,
	'application': True,
	'auto_install': False,
    'sequence': 3,
}