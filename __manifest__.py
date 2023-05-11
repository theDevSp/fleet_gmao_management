# -*- coding: utf-8 -*-
{
    'name': "fleet_gmao_management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_fiscal_year_period', 'fleet','construction_site_management'],

    # always loaded
    'data': [
		'security/security_groups.xml',
		'security/ir.model.access.csv',
		'views/vehicle_views.xml',
		'views/vehicle_docs_views.xml',
		'views/checklist_view.xml',
		'views/filtre_view.xml',
		'views/fleet_vehicle_activity.xml',
		'views/templates.xml',
	],
    'installable': True,
	'application': True,
	'auto_install': False
}
