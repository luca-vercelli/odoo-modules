# -*- encoding: utf-8 -*-
##############################################################################
#
# Released under LGPL v.3
#
##############################################################################

{
    "name": "Database Manager",
    "version": "1.0.1",
    "category": "Configuration",
    "description": """
		Allow execution of arbitrary SQL commands on DB.
		
		This module can be useful in order to execute **simple** queries/updates on database without direct access to server, and/or without PgAdmin installed.
		
		The module create a new menu "Configuration" -> "Technical" -> "DB Manager", that is visible only in development mode.
		Only members of group "Database (SQL) manager" can use it.
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
