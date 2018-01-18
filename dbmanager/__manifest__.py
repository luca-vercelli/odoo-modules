# -*- encoding: utf-8 -*-
##############################################################################
#
# Released under LGPL v.3
#
##############################################################################

{
    "name": "Database Manager",
    "version": "1.0",
    "category": "Configuration",
    "description": """
		Allow execution of arbitrary SQL commands on DB.
		
		This module can be useful in order to execute **simple** queries/updates on database without direct access to server, and/or without PgAdmin installed.
		""",
    "author": "Luca Vercelli - Finsoft srl",
    "website": "",
    "depends": [
        "base"
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/create_views.sql',
    ],
    "init_xml": [],
    "update_xml": [],
    "demo_xml": [],
    "test": [],
    "installable": True,
    "active": False,
	"license" : 'LGPL-3',
	"application" : False,
}
