# -*- coding: utf-8 -*-
# Copyright (c) 2007 Ferran Pegueroles <ferran@pegueroles.com>
# Copyright (c) 2009 Albert Cervera i Areny <albert@nan-tic.com>
# Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
# Copyright (C) 2013-2014 Camptocamp (<http://www.camptocamp.com>)
# Copyright (C) 2017 Finsoft srl (<http://www.finsoft.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Report to printer - Windows Version",
    'version': '10.0.1.0.2',
    'category': 'Generic Modules/Base',
    'author': "Luca Vercelli - Finsoft srl",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends": ['report'],
    'data': [
        'data/printing_data.xml',
        'security/security.xml',
        'views/assets.xml',
        'views/printing_printer_view.xml',
        #'views/printing_server.xml',
        #'views/printing_job.xml',
        'views/printing_report_view.xml',
        'views/res_users_view.xml',
        'views/ir_actions_report_xml_view.xml',
        #'wizards/printing_printer_update_wizard_view.xml',
        'views/ghostscript.xml',
    ],
	# FIXME is Debian-like 'conflicts' supported?
    'conflicts': ['base_report_to_printer'],
	# FIXME is Debian-like 'provides' supported?
    'provides': ['base_report_to_printer'],
    'installable': True,
    'application': True,
    'external_dependencies': {
        'python': ['subprocess32'],
		#FIXME should Ghostscript/GSView be listed here?
    },
}
