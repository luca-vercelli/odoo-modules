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

import os
DIRNAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
	
def write_to_new_tempfile(self, data, prefix='', suffix='.tmp', dir=None, delete=True):
    """
    Create a new file, write 'data' into it, close it
    @return filename
    """
    import tempfile
    fd = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, dir=dir, delete=delete)
    fd.write(data)
    fd.close()
    return fd.name

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

def test_xsd(xml_filename, xsd_filename):
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

