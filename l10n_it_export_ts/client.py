#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (C) 2016 luca Vercelli
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from . import util

if __name__ == "__main__":

	#Utenza di test. A oggi (25-12-2016) mi paiono disabilitate.
	CF_PROPRIETARIO="MTOMRA66A41G224M"
	PI_PROPRIETARIO="65498732105"
	PASSWORD="Salve123"
	FILENAME="file1.xml"
	PINCODE_INVIANTE="3489543096"
	TEST=True

	print("Lettura file di configurazione...")
	from .properties import *

	#solo ricevuta
	if 1 == 2:
		answer3, pdf_filename = util.call_ws_ricevuta(PINCODE_INVIANTE, 16122814390642472, CF_PROPRIETARIO, PASSWORD)
		print("Ricevuta PDF salvata in:", pdf_filename)
		import os
		os.system("xdg-open " + str(pdf_filename))
		die

	#solo dettaglio errori
	if 1 == 2:
		answer3, csv_filename = util.call_ws_dettaglio_errori(PINCODE_INVIANTE, 16122814390642472, CF_PROPRIETARIO, PASSWORD)
		print("Ricevuta CSV salvata in:", csv_filename)
		import os
		os.system("xdg-open " + str(csv_filename))
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

#TRE INVII HANNO AVUTO SUCCESSO: 16122814390642472, 16122816595143484, 16122821562546770
	print("Termino.")
