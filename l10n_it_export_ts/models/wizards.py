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

    proprietario_id = fields.Many2one('res.partner',string='Proprietario')

    @api.multi
    def export(self):
        """
        I can export many invoices, neverthless I get a single Export object
        """
        now = fields.Datetime.now()
 
        invoices = self.env['account.invoice'].browse(self.env.context['active_ids'])
        companies = [i.number for i in invoices if i.partner_id.is_company]
        oppositions = [i.number for i in invoices if i.partner_id.opposizione_730]
        messages = ""
        if companies:
            messages = messages + "Fatture ignorate perchè non intestate a persone fisiche: " + str(companies) + "\r\n"
        if oppositions:
            messages = messages + "Fatture ignorate perchè intestatario oppostosi alla dichiarazione TS: " + str(oppositions) + "\r\n"
        
        ctx = self.env.context
        values = {
            'doc_ids' : ctx['active_ids'],
            'doc_model' : ctx['active_model'],
            'docs' : self.env[ctx['active_model']].browse(ctx['active_ids']),
            'proprietario' : self.proprietario_id
        }

        result = self.env['ir.actions.report'].render_template('l10n_it_export_ts.qweb_invoice_xml_ts', values)

        self.env['exportts.export.registry'].create({
            'proprietario_id' : self.proprietario_id.id,
            'status' : 'Exported',
            'xml' : result,
            'date_export' : now,
            'messages': messages
            })

#See:

# <<Il trattamento e la conservazione del codice fiscale dell'assistito,
#rilevato dalla Tessera Sanitaria, crittografato secondo le
#modalita' di cui al decreto attuativo del comma 5 dell'articolo 50
#del DL 269/2003, utilizzando la chiave pubblica RSA contenuta
#nel certificato X.509 fornito dal sistema TS ed applicando il
#padding PKCS#1 v 1.5. Tale trattamento deve essere eseguito
#tramite procedure automatizzate all'atto della memorizzazione
#negli archivi locali.>>

# i due indirizzi sono questi:
# URL_TEST="https://invioss730ptest.sanita.finanze.it/InvioTelematicoSS730pMtomWeb/InvioTelematicoSS730pMtomPort"
# URL_PROD="https://invioss730p.sanita.finanze.it/InvioTelematicoSS730pMtomWeb/InvioTelematicoSS730pMtomPort"
# il problema e' che ?wsdl *non* viene reso disponibile via web
# quindi abbiamo i due file WSDL in locale:

import os
DIRNAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

XSD_FILENAME = os.path.join(DIRNAME, "data", "730_precompilata.xsd")
WSDL_PROD = os.path.join(DIRNAME, "data", "InvioTelematicoSpeseSanitarie730p.wsdl")
WSDL_TEST = os.path.join(DIRNAME, "data", "InvioTelematicoSpeseSanitarie730pTest.wsdl")
WSDL_ESITO = os.path.join(DIRNAME, "data", "EsitoInvioDatiSpesa730Service.wsdl")
WSDL_DET_ERRORI = os.path.join(DIRNAME, "data", "DettaglioErrori730Service.wsdl")
WSDL_RICEVUTE = os.path.join(DIRNAME, "data", "RicevutaPdf730Service.wsdl")



class WizardSendToTS(models.TransientModel):
    _name = "exportts.wizard.send"
    _description = "Invia XML a Sistema TS"

    pincode_inviante = fields.Char('PINCODE inviante', required=True)
    password_inviante = fields.Char('Password', required=True)
    endpoint = fields.Selection([('P','Produzione'),('T','Test')], required=True)
    #esportazione_id = fields.Many2one('exportts.export.registry', 'Esportazione', required=True)
    
    
    @api.one
    def solo_ricevuta(self): #non usato?
        export = self.env['exportts.export.registry'].browse(self.env.context['active_id'])
        cf_proprietario = export.proprietario_id.fiscalcode # TODO puoi prendere quello già criptato
        from . import util
        answer3, pdf_filename = self.call_ws_ricevuta(self.pincode_inviante, 16122814390642472, cf_proprietario, self.password_inviante)
        self.pdf_filename = pdf_filename
        print("Ricevuta PDF salvata in:", pdf_filename)
        #os.system("xdg-open " + str(pdf_filename))

    @api.one
    def solo_dettaglio_errori(self): #non usato?
        export = self.env['exportts.export.registry'].browse(self.env.context['active_id'])
        cf_proprietario = export.proprietario_id.fiscalcode # TODO puoi prendere quello già criptato
        from . import util
        answer3, csv_filename = self.call_ws_dettaglio_errori(self.pincode_inviante, 16122814390642472, cf_proprietario, self.password_inviante)
        self.csv_filename = csv_filename
        print("Ricevuta CSV salvata in:", csv_filename)
        #os.system("xdg-open " + str(csv_filename))

    def write_to_new_tempfile(self, data):
        import tempfile
        xmlfile = tempfile.NamedTemporaryFile()
        xmlfile.write(data)
        xmlfile.close()
        return xmlfile.name
        
    @api.one
    def send(self):
        export = self.env['exportts.export.registry'].browse(self.env.context['active_id'])
        cf_proprietario = export.proprietario_id.fiscalcode # TODO puoi prendere quello già criptato
        xmlfilename = self.write_to_new_tempfile(export.xml)
        TEST = (self.endpoint == 'T')

        from . import util
        print("Validating...")
        util.test_xsd(xmlfilename, XSD_FILENAME)
        print("Compressione dati...")
        zipfilename = util.zip_single_file(xmlfilename)
        
        print("Invio dati...")
        answer = self.call_ws_invio(zipfilename, self.pincode_inviante, cf_proprietario, self.password_inviante, TEST)

        print("Invio concluso. Risposta:")
        print(answer)

        if answer.protocollo:
            protocollo = answer.protocollo
            
            import time
            time.sleep(4)
            print("Esito invio:")
            answer2 = self.call_ws_esito(self.pincode_inviante, protocollo, cf_proprietario, self.password_inviante)
            print(answer2)
            
            answer3, pdf_filename = self.call_ws_ricevuta(self.pincode_inviante, protocollo, cf_proprietario, self.password_inviante)
            print("Ricevuta PDF salvata in:", pdf_filename)
            self.pdf_filename = pdf_filename
            #import os
            #if pdf_filename is not None:
            #    os.system("xdg-open " + str(pdf_filename))
            
            answer4, csv_filename = util.call_ws_dettaglio_errori(self.pincode_inviante, protocollo, cf_proprietario, self.password_inviante)
            print("Dettaglio errori CSV salvato in:", csv_filename)
            self.csv_filename = csv_filename
            #import os
            #if csv_filename is not None:
            #    os.system("xdg-open " + str(csv_filename))

    def call_ws_invio(self, zipfilename, pincode_inviante, cf_proprietario, pwd, if_test):
	    """
	    Call the webservice "inviaFileMtom()".
	    Fill all required parameters: file name, file content, owner data, basic auth. credentials
	    Currently, require a modified version of osa (as we need Basic Authentication)
	    Currently, MTOM protocol is not used, file is sent as part of the message.
	    
	    @return webservice answer, which is an object of type "inviaFileMtomResponse"
	    """

        from .. import osa

	    global WSDL_PROD, WSDL_TEST
	    if if_test:
		    wsdl = WSDL_TEST
	    else:
		    wsdl = WSDL_PROD

	    cl = osa.Client(wsdl)

	    parameters = cl.types.inviaFileMtom()
	    parameters.nomeFileAllegato = os.path.basename(zipfilename)
	    parameters.pincodeInvianteCifrato = encrypt(pincode_inviante)
	    parameters.datiProprietario = cl.types.proprietario()
	    parameters.datiProprietario.cfProprietario = cf_proprietario	#cleartext
	    parameters.documento = open(zipfilename, "r").read()

	    cl.service.inviaFileMtom.set_auth(cf_proprietario, pwd)

	    return cl.service.inviaFileMtom(parameters)

    #Questa era una delle risposte:
    #(ricevutaInvio){
    #    codiceEsito = 000
    #    dataAccoglienza = 25-12-2016 22:24:20
    #    descrizioneEsito = Il file  in attesa di elaborazione, per conoscerne l'esito  necessario verificare la ricevuta
    #    dimensioneFileAllegato = 24922
    #    nomeFileAllegato = file1.xmlI4c52M.zip
    #    protocollo = 16122522242096203
    #    idErrore = 
    #}

    def call_ws_esito(self, pincode_inviante, protocollo, cf_proprietario, pwd):
	    """
	    Call the webservice "EsitoInvii()".
	    Restituisce l'esito dell'invio corrispondente al numero di protocollo dato
	    @return webservice answer
	    """
	    global WSDL_ESITO

        from .. import osa

	    wsdl = WSDL_ESITO
	    cl = osa.Client(wsdl)

	    parameters = cl.types.EsitoInvii()
	    parameters.DatiInputRichiesta = cl.types.datiInput()
	    parameters.DatiInputRichiesta.pinCode = encrypt(pincode_inviante)
	    parameters.DatiInputRichiesta.protocollo = protocollo
	    #alternativi al protocollo:
	    #parameters.DatiInputRichiesta.dataInizio = '24-12-2016'
	    #parameters.DatiInputRichiesta.dataFine = '26-12-2016'

	    cl.service.EsitoInvii.set_auth(cf_proprietario, pwd)

	    return cl.service.EsitoInvii(parameters)

    #Questa era una delle risposte:
    #(datiOutput){
    #    esitoChiamata = 0
    #    descrizioneEsito =  
    #    esitiPositivi = (esitiPositivi){
    #                        dettagliEsito[] = [
    #                                           (dettaglioEsitoPositivo){
    #                                               protocollo = 16122522242096203
    #                                               dataInvio = 25-12-2016 22:24:20
    #                                               stato = 5
    #                                               descrizione = File scartato in fase di Elaborazione
    #                                               nInviati = 0
    #                                               nAccolti = 0
    #                                               nWarnings = 0
    #                                               nErrori = 0
    #                                           }
    #                                           ]
    #                    }
    #    esitiNegativi = None (esitiNegativi)
    #}

    def call_ws_dettaglio_errori(self, pincode_inviante, protocollo, cf_proprietario, pwd):
	    """
	    Call the webservice "DettaglioErrori()".
	    Restituisce un CSV contenente il dettaglio degli errori di importazione
	    @return (webservice answer, csv_filename)
	    """
	    global WSDL_DET_ERRORI

        from .. import osa

	    wsdl = WSDL_DET_ERRORI
	    cl = osa.Client(wsdl)

	    parameters = cl.types.DettaglioErrori()
	    parameters.DatiInputRichiesta = cl.types.datiInput()
	    parameters.DatiInputRichiesta.pinCode = encrypt(pincode_inviante)
	    parameters.DatiInputRichiesta.protocollo = protocollo

	    cl.service.DettaglioErrori.set_auth(cf_proprietario, pwd)

	    answer = cl.service.DettaglioErrori(parameters)

	    csv_filename = None
	    try:
		    if answer.esitiPositivi.dettagliEsito.csv:
			    import tempfile
			    boh, csv_filename = tempfile.mkstemp(prefix="errori", suffix=".csv.zip")
			    fd = open(csv_filename,"w")
			    fd.write(answer.esitiPositivi.dettagliEsito.csv)
			    fd.close()
	    except:
		    pass
	    return (answer, csv_filename)

    #Questa era una delle risposte:
    #(datiOutput){
    #    esitoChiamata = 1
    #    esitiPositivi = None (esitiPositivi)
    #    esitiNegativi = (esitiNegativi){
    #                        dettaglioEsitoNegativo[] = [
    #                                                    (dettaglioEsitoNegativo){
    #                                                        codice = WS37
    #                                                        descrizione = FILE SCARTATO, CONTROLLARE LA RICEVUTA PDF
    #                                                    }
    #                                                    ]
    #                    }
    #}

    def call_ws_ricevuta(self, pincode_inviante, protocollo, cf_proprietario, pwd):
	    """
	    Call the webservice "RicevutaPdf()".
	    Restituisce la ricevuta dell'invio corrispondente al numero di protocollo dato
	    @return (webservice answer, local PDF temp file)
	    """
	    global WSDL_RICEVUTE

        from .. import osa

	    wsdl = WSDL_RICEVUTE
	    cl = osa.Client(wsdl)

	    parameters = cl.types.RicevutaPdf()
	    parameters.DatiInputRichiesta = cl.types.datiInput()
	    parameters.DatiInputRichiesta.pinCode = encrypt(pincode_inviante)
	    parameters.DatiInputRichiesta.protocollo = protocollo

	    cl.service.RicevutaPdf.set_auth(cf_proprietario, pwd)

	    answer = cl.service.RicevutaPdf(parameters)

	    pdf_filename = None
	    if answer.esitiPositivi and answer.esitiPositivi.dettagliEsito and answer.esitiPositivi.dettagliEsito.pdf:
		    import tempfile
		    boh, pdf_filename = tempfile.mkstemp(prefix="ricevuta", suffix=".pdf")
		    fd = open(pdf_filename,"w")
		    fd.write(answer.esitiPositivi.dettagliEsito.pdf)
		    fd.close()
	    
	    return (answer, pdf_filename)


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

