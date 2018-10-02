# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 luca Vercelli
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models,fields,api

#see /usr/lib/python2.7/dist-packages/openerp/addons/product/product.py

 
class ExportRegistry(models.Model):
    _name = 'exportts.export.registry'
    _description = 'Esportazioni TS'

    date = fields.Date('Last day of month of run')
    status = fields.Char()
    xml = fields.Char()

class DialogExportToXML(models.TransientModel):
    """
    Esporterei in cartella opportuna, come export-ts-YYYY-MM-DD.xml
    """
    _name = "exportts.export"
    _description = "Estrai fatture in XML"

    @api.one
    def export(self):
        pass

class DialogSendToTS(models.TransientModel):
    _name = "exportts.send"
    _description = "Invia XML a Sistema TS"

    cf_proprietario = fields.Char('C.F. Proprietario')
    pi_proprietario = fields.Char('P.IVA Proprietario')
    pincode_inviante = fields.Integer('PINCODE inviante')
    password_inviante = fields.Char('Password')
    url = fields.Char('URL', default='http://example.com')

    @api.one
    def send(self):
        pass
    
    @api.one
    def solo_ricevuta(self): #non usato?
	    answer3, pdf_filename = util.call_ws_ricevuta(PINCODE_INVIANTE, 16122814390642472, CF_PROPRIETARIO, PASSWORD)
	    print("Ricevuta PDF salvata in:", pdf_filename)
	    import os
	    os.system("xdg-open " + str(pdf_filename))
	    die

    @api.one
    def solo_dettaglio_errori(self): #non usato?
	    answer3, csv_filename = util.call_ws_dettaglio_errori(PINCODE_INVIANTE, 16122814390642472, CF_PROPRIETARIO, PASSWORD)
	    print("Ricevuta CSV salvata in:", csv_filename)
	    import os
	    os.system("xdg-open " + str(csv_filename))
	    die

    def vecchia_gestione_filename(self, FILENAME):
        die
        if FILENAME is None:
	        raise ValueError("FILENAME not set")
        FILENAME = str(FILENAME)
        if FILENAME.lower().endswith(".xml"):
	        print("Converting uppercase & lowercase...")
	        util.upperLowerCase(FILENAME)
	        print("Validating...")
	        util.test_xsd(FILENAME)
	        print("Compressione dati...")
	        zipfilename = util.zip_single_file(FILENAME)
        elif FILENAME.lower().endswith(".zip"):
	        zipfilename = FILENAME
        else:
	        raise ValueError("FILENAME must be .xml or .zip")
        
        print("Invio dati...")
        answer = util.call_ws_invio(zipfilename, PINCODE_INVIANTE, CF_PROPRIETARIO, PASSWORD, TEST)

        print("Invio concluso. Risposta:")
        print(answer)

        if answer.protocollo:
	        protocollo = answer.protocollo
	        
	        import time
	        time.sleep(4)
	        print("Esito invio:")
	        answer2 = util.call_ws_esito(PINCODE_INVIANTE, protocollo, CF_PROPRIETARIO, PASSWORD)
	        print(answer2)
	        
	        answer3, pdf_filename = util.call_ws_ricevuta(PINCODE_INVIANTE, protocollo, CF_PROPRIETARIO, PASSWORD)
	        print("Ricevuta PDF salvata in:", pdf_filename)
	        import os
	        if pdf_filename is not None:
		        os.system("xdg-open " + str(pdf_filename))
	        
	        answer4, csv_filename = util.call_ws_dettaglio_errori(PINCODE_INVIANTE, protocollo, CF_PROPRIETARIO, PASSWORD)
	        print("Dettaglio errori CSV salvato in:", csv_filename)
	        import os
	        if csv_filename is not None:
		        os.system("xdg-open " + str(csv_filename))


