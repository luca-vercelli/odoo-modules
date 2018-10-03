# -*- encoding: utf-8 -*-
##############################################################################
#
# Released under GPL v.2
#
##############################################################################

{
    "name": "Marca da bollo.",
    "version": "1.2",
    "category": "Accounting",
    "description": """
      Addebita la marca da bollo in fattura, in maniera ingenua: sempre, se l'importo è sufficiente.

      Dopo aver installato il modulo, occorre configurarlo:

      * selezionare il flag "addebita marca da bollo" sui clienti opportuni

      * impostare il conto della tassa marca da bollo, dal menù Imposte. Ad esempio il 260100 (IVA n/debito) dovrebbe funzionare, anche se non è molto corretto.
      
      * Il valore limite di default è 77,47€, si può modificare tramite il menu Imposte
      
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
