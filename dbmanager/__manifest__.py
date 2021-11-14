# -*- encoding: utf-8 -*-
##############################################################################
#
# Released under LGPL v.3
#
##############################################################################

{
    "name": "Database Manager",
    "version": "1.0.5",
    "category": "Configuration",
    "description": "",
    "author": "Luca Vercelli - Finsoft srl",
    "website": "",
    "summary": "Allow execution of arbitrary SQL commands on DB",
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
    "application" : False,  #should be True, however README.rst won't be shown !?!
}
