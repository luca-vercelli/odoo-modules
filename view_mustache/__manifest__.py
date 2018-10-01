# -*- encoding: utf-8 -*-
##############################################################################
#
# Released under LGPL v.3
#
##############################################################################

{
    "name": "Mustache views",
    "version": "1.1",
    "category": "Base",
    "author": "Luca Vercelli - Finsoft srl",
    "website": "",
    "depends": [ "base", "account" ],
    'data': [
        'report_invoice/report_invoice.xml',
    ],
    "init_xml": [],
    "update_xml": [],
    "demo_xml": [],
    "test": [],
    "installable": True,
    "active": False,
	'license' : 'LGPL-3',
    'external_dependencies': {
        'python': ['pystache'],
    },
}
