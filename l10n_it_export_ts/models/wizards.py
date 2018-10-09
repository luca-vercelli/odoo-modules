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

import os

class WizardExportInvoices(models.TransientModel):
    _name = "exportts.wizard.export"
    _description = "Esporta fatture in XML"

    @api.multi
    def export(self):
        """
        I can export many invoices, neverthless I get a single Export object
        """
        now = fields.Datetime.now()
        filename = 'export-ts-' + now + '.xml'

        invoices = self.env['account.invoice'].browse(self.env.context.active_ids)
        companies = [i.number for i in invoices if i.partner_id.is_company]
        oppositions = [i.number for i in invoices if i.partner_id.opposizione_730]
        messages = ""
        if companies:
            messages = messages + "Fatture ignorate perchè non intestate a persone fisiche: " + str(companies) + "\r\n"
        if oppositions:
            messages = messages + "Fatture ignorate perchè intestatario oppostosi alla dichiarazione TS: " + str(oppositions) + "\r\n"
        
        #import pdb
        #pdb.set_trace()

        #come passo i numeri di fatture? in self.env.context.active_ids
        result = self.env['ir.actions.report'].render_template('l10n_it_export_ts.qweb_invoice_xml_ts')

        self.env['exportts.export.registry'].create({
            'status' : 'Exported',
            'xml' : result,
            'date_export' : now,
            'messages': messages
            })

class WizardSendToTS(models.TransientModel):
    _name = "exportts.wizard.send"
    _description = "Invia XML a Sistema TS"

    cf_proprietario = fields.Char('C.F. Proprietario', required=True)
    pi_proprietario = fields.Char('P.IVA Proprietario', required=True)
    pincode_inviante = fields.Char('PINCODE inviante', required=True)
    password_inviante = fields.Char('Password', required=True)
    endpoint = fields.Selection([('P','Produzione'),('T','Test')], required=True)
    #esportazione_id = fields.Many2one('exportts.export.registry', 'Esportazione', required=True)
    
    
    @api.one
    def solo_ricevuta(self): #non usato?
        from . import util
        answer3, pdf_filename = util.call_ws_ricevuta(self.pincode_inviante, 16122814390642472, self.cf_proprietario, self.password_inviante)
        self.pdf_filename = pdf_filename
        print("Ricevuta PDF salvata in:", pdf_filename)
        #os.system("xdg-open " + str(pdf_filename))

    @api.one
    def solo_dettaglio_errori(self): #non usato?
        from . import util
        answer3, csv_filename = util.call_ws_dettaglio_errori(self.pincode_inviante, 16122814390642472, self.cf_proprietario, self.password_inviante)
        self.csv_filename = csv_filename
        print("Ricevuta CSV salvata in:", csv_filename)
        #os.system("xdg-open " + str(csv_filename))

    def write_to_file(self, data):
        import tempfile
        xmlfile = tempfile.NamedTemporaryFile()
        xmlfile.write(data)
        xmlfile.close()
        return xmlfile.name
        
    @api.one
    def send(self):
        xmlfilename = self.write_to_file(self.esportazione_id.xml)
        TEST = (self.endpoint == 'T')

        from . import util
        print("Converting uppercase & lowercase...")
        #TODO spostare altrove?
        util.upperLowerCase(xmlfilename)
        print("Validating...")
        util.test_xsd(xmlfilename)
        print("Compressione dati...")
        zipfilename = util.zip_single_file(xmlfilename)
        
        print("Invio dati...")
        answer = util.call_ws_invio(zipfilename, self.pincode_inviante, self.cf_proprietario, self.password_inviante, TEST)

        print("Invio concluso. Risposta:")
        print(answer)

        if answer.protocollo:
            protocollo = answer.protocollo
            
            import time
            time.sleep(4)
            print("Esito invio:")
            answer2 = util.call_ws_esito(self.pincode_inviante, protocollo, self.cf_proprietario, self.password_inviante)
            print(answer2)
            
            answer3, pdf_filename = util.call_ws_ricevuta(self.pincode_inviante, protocollo, self.cf_proprietario, self.password_inviante)
            print("Ricevuta PDF salvata in:", pdf_filename)
            self.pdf_filename = pdf_filename
            #import os
            #if pdf_filename is not None:
            #    os.system("xdg-open " + str(pdf_filename))
            
            answer4, csv_filename = util.call_ws_dettaglio_errori(self.pincode_inviante, protocollo, self.cf_proprietario, self.password_inviante)
            print("Dettaglio errori CSV salvato in:", csv_filename)
            self.csv_filename = csv_filename
            #import os
            #if csv_filename is not None:
            #    os.system("xdg-open " + str(csv_filename))

class WizardEncryptAllFiscalCodes(models.TransientModel):
    _name = "res.partner.encrypt"
    _description = "Encrypt fiscal codes"

    @api.one
    def encrypt_all_fiscalcodes(self):
        """
        This encrypts all fiscalcode on demand.
        """
        from . import util
        model = self.env['res.partner']
        all_partners = model.search([])
        for record in all_partners:
            if record.fiscalcode:
                record.fiscalcode_enc = util.encrypt(record.fiscalcode)
            else:
                record.fiscalcode_enc = None

