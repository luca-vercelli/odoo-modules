#!/usr/bin/env python
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

# Dal momento che non riesco a criptare i campi via GUI, lo faccio da qua :(
# Forse si potrebbe fare in un batch?

import logging
import urllib.parse
import uuid
import psycopg2.extras
import psycopg2.extensions
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_READ_COMMITTED, ISOLATION_LEVEL_REPEATABLE_READ
from psycopg2.pool import PoolError

from . import util

if __name__ == "__main__":
	dbusername = 'odoo'
	dbname = 'daniela'
	#will connect with no password. So, this script must be run with "sudo -u odoo ./crypth_all.py"
	dsn = " user=%s dbname=%s "%(dbusername,dbname)

	dati = []

	connection = psycopg2.connect(dsn=dsn, autocommit=True, connection_factory=psycopg2.extensions.connection)
	cursor = connection.cursor()
	cursor.execute("SELECT id, name, fiscalcode FROM res_partner WHERE fiscalcode IS NOT NULL ORDER BY id")
	for id, name, fiscalcode in cursor.fetchall() :
		dati.append([id, name, util.encrypt(fiscalcode)])
	
	for [id, name, enc] in dati:
		query = "UPDATE res_partner SET fiscalcode_enc= '%s' WHERE id = %s " % (enc, id)
		print("Encrypting customer n.", id, name)
		cursor.execute(query)

	connection.commit()
	connection.close()

