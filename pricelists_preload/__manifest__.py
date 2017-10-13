# -*- encoding: utf-8 -*-
##############################################################################
#
# Released under LGPL v.3
#
##############################################################################

{
    "name": "Carica listini",
    "version": "1.0",
    "category": "Sales",
    "description": """
		Load into a pricelist rows for all product variants with some given attribute.
		
		Inside the pricelist you'll find a new action "Prepare pricelists". You'll be asked to specify a
		product attribute value, and the program will find all variant products with the specified attribute value.
		
		Configuration: set Attribute in Sales configuration settings.
		
		""",
    "author": "Luca Vercelli - Finsoft srl",
    "website": "",
    "depends": [
        "product", "variant_search"
    ],
    'data': [
        'views/new_button.xml',
        'views/res_config.xml',
    ],
    "init_xml": [],
    "update_xml": [],
    "demo_xml": [],
    "test": [],
    "installable": True,
    "active": False,
	'license' : 'LGPL-3',
}
