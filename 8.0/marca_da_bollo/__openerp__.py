# -*- encoding: utf-8 -*-
##############################################################################
#
# Released under GPL v.2
#
##############################################################################

{
    "name": "Marca da bollo.",
    "version": "1.0",
    "category": "Accounting",
    "description": """
      Addebita la marca da bollo in fattura, in maniera ingenua: sempre, se l'importo è sufficiente.
      Dopo aver installato il modulo, occorre configurare il conto della tassa marca da bollo, altrimenti
      risulterà sbagliato il 'Saldo' di ogni fattura.
      """,
    "author": "Luca Vercelli",
    "website": "",
    "depends": [
        "account",
    ],
    "init_xml": [],
    "update_xml": [
        "account_tax_view.xml",
        "account_tax_data.xml",
    ],
    "demo_xml": [],
    "test": [],
    "installable": True,
    "active": False,
}
