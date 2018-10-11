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

from .. import osa

#See:
#http://www.rgs.mef.gov.it/VERSIONE-I/Attivit--i/Spesa-soci/Progetto-T/
#http://sistemats1.sanita.finanze.it/wps/wcm/connect/ea33a237-e840-4cdc-8a62-3a763831cf83/DM+31+luglio+2015.pdf?MOD=AJPERES&CACHEID=ea33a237-e840-4cdc-8a62-3a763831cf83
#http://sistemats1.sanita.finanze.it/wps/wcm/connect/487b0bba-6a65-42f9-8b43-2fb907fe7e91/730+Spese+Sanitarie+-+WS+Asincrono+-+Invio+dati+di+spesa++sanitaria+%2819+settembre+2016%29.pdf?MOD=AJPERES&CACHEID=487b0bba-6a65-42f9-8b43-2fb907fe7e91
#
#kit:
#http://sistemats1.sanita.finanze.it/wps/wcm/connect/0f7a758c-9638-4e74-95b7-bde0bfab29a5/kit730P_ver_20161117.zip?MOD=AJPERES&CACHEID=0f7a758c-9638-4e74-95b7-bde0bfab29a5

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

PUBLIC_KEY_PEM_FILENAME = os.path.join(DIRNAME, "data", "SanitelCF.cer")
PUBLIC_KEY = None

def get_pubkey():
	"""
	Extract public RSA key from X.509 PEM certificate specified by PUBLIC_KEY_PEM_FILENAME
	"""
	#see http://stackoverflow.com/questions/12911373/how-do-i-use-a-x509-certificate-with-pycrypto
	global PUBLIC_KEY
	if PUBLIC_KEY is None:
		global PUBLIC_KEY_PEM_FILENAME
		from Crypto.Util.asn1 import DerSequence
		from Crypto.PublicKey import RSA
		from binascii import a2b_base64

		# Convert from PEM to DER
		pem = open(PUBLIC_KEY_PEM_FILENAME).read()
		lines = pem.replace(" ",'').split()
		der = a2b_base64(''.join(lines[1:-1]))

		# Extract subjectPublicKeyInfo field from X.509 certificate (see RFC3280)
		cert = DerSequence()
		cert.decode(der)
		tbsCertificate = DerSequence()
		tbsCertificate.decode(cert[0])
		subjectPublicKeyInfo = tbsCertificate[6]

		# Initialize RSA key
		PUBLIC_KEY = RSA.importKey(subjectPublicKeyInfo)
	return PUBLIC_KEY

def encrypt(message):
	"""
	Encrypt emessage using given RSA public key, padding PKCS#1 v1.5, encoding base64
	"""
	#see https://www.dlitz.net/software/pycrypto/api/2.6/
	#cfr. echo "message" | openssl rsautl -encrypt -inkey SanitelCF.cer -certin -pkcs | base64
	#SanitelCF.cer non e' una chiave RSA ma un certificato che contiene una chiave RSA (pubblica)
	#padding PKCS1_v1_5 = sequenza causale di byte per raggiungere la lunghezza della chiave RSA
	#base64 = binary to ASCII

	#Python 2:
	#try:
	#	message = str(message)
	#except UnicodeDecodeError:
	#	message = message.encode('ascii','replace')

	#Python 3:
	message = message.encode()

	from Crypto.Cipher import PKCS1_v1_5
	from Crypto.Hash import SHA
	import base64

	h = SHA.new(message)
	key = get_pubkey()
	cipher = PKCS1_v1_5.new(key)
	msg_enc = cipher.encrypt(message)
	return base64.encodestring(msg_enc)
	
def zip_single_file(orig_filename):
	"""
	Compress single file to a temporary location.
	ZIP File will be deleted on exit.

	@return ZIP full file name
	"""
	import tempfile
	fd, zip_filename = tempfile.mkstemp(prefix=orig_filename, suffix=".zip")
	from zipfile import ZipFile
	zf = ZipFile(zip_filename, "w") #overwrite if exists
	zf.write(orig_filename)
	zf.close()
	return zip_filename
	
def call_ws_invio(zipfilename, pincode_inviante, cf_proprietario, pwd, if_test):
	"""
	Call the webservice "inviaFileMtom()".
	Fill all required parameters: file name, file content, owner data, basic auth. credentials
	Currently, require a modified version of osa (as we need Basic Authentication)
	Currently, MTOM protocol is not used, file is sent as part of the message.
	
	@return webservice answer, which is an object of type "inviaFileMtomResponse"
	"""
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

def call_ws_esito(pincode_inviante, protocollo, cf_proprietario, pwd):
	"""
	Call the webservice "EsitoInvii()".
	Restituisce l'esito dell'invio corrispondente al numero di protocollo dato
	@return webservice answer
	"""
	global WSDL_ESITO

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

def call_ws_dettaglio_errori(pincode_inviante, protocollo, cf_proprietario, pwd):
	"""
	Call the webservice "DettaglioErrori()".
	Restituisce un CSV contenente il dettaglio degli errori di importazione
	@return (webservice answer, csv_filename)
	"""
	global WSDL_DET_ERRORI

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

def call_ws_ricevuta(pincode_inviante, protocollo, cf_proprietario, pwd):
	"""
	Call the webservice "RicevutaPdf()".
	Restituisce la ricevuta dell'invio corrispondente al numero di protocollo dato
	@return (webservice answer, local PDF temp file)
	"""
	global WSDL_RICEVUTE

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

def test_xsd(xml_filename, xsd_filename=XSD_FILENAME):
	"""
	Test XML against XSD schema.
	Raise exception with details if validation fails. 
	"""
	from lxml import etree
	xmlschema_doc = etree.parse(xsd_filename)
	xmlschema = etree.XMLSchema(xmlschema_doc)
	doc = etree.parse(xml_filename)
	#return xmlschema.validate(doc)
	xmlschema.assertValid(doc)

def upperLowerCase(xml_filename):
	"""
	I tag XML sono attesi case sensitive, invece Odoo li genera tutti minuscoli
	Questa implementazione esegue SED, e richiede l'opzione s/././I, quindi funziona solo in Linux
	"""
	TAGS = ['cfProprietario','documentoSpesa','idSpesa','pIva','dataEmissione','numDocumentoFiscale','numDocumento','dataPagamento','flagOperazione','cfCittadino','voceSpesa','tipoSpesa']
	SED = "sed -i "
	for tag in TAGS:
		SED += " -e s/%s/%s/I " % (tag, tag)
	SED += xml_filename
	try:
		print("Executing ", SED)
		os.system(SED)
	except:
		print("Errore nella conversione di maiuscole e minuscole, il file potrebbe venire rifiutato")

