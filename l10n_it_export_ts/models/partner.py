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

from odoo import models,fields,api

#see /usr/lib/python2.7/dist-packages/openerp/addons/account/partner.py

class res_partner(models.Model):
	_inherit = 'res.partner'

	fiscalcode = fields.Char(inverse='_encrypt_fiscalcode_inverse')
	fiscalcode_enc = fields.Char()
	opposizione_730 = fields.Boolean("Opposizione alla dichiarazione 730")

	@api.depends('fiscalcode')	
	def _encrypt_fiscalcode(self):
		"""
		This should encrypt fiscalcode "on the fly" during report export.
		Bad choice.
		"""
		from . import util
		for record in self:
			if self.fiscalcode is None:
				self.fiscalcode_enc = None
			else:
				record.fiscalcode_enc = util.encrypt(record.fiscalcode)

	def _encrypt_fiscalcode_inverse(self):
		"""
		This encrypts fiscalcode whenever it is changed and saved. 
		"""
		from . import util
		for record in self:
			if record.fiscalcode is None:
				record.fiscalcode_enc = None
			else:
				record.fiscalcode_enc = util.encrypt(record.fiscalcode)

	@api.v8
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
	@api.v7
	def encrypt_all_fiscalcodes_v7(self, cr, uid, context={}):
		"""
		This encrypts all fiscalcode on demand, inside batch queue.
		"""
		#FIXME apparently, batches require API v7
		from . import util
		model = self.pool['res.partner']
		ids = model.search(cr, uid, [], context=context)
		for record in model.browse(cr, uid, ids, context=context):
			if record.fiscalcode:
				record.fiscalcode_enc = util.encrypt(record.fiscalcode)
			else:
				record.fiscalcode_enc = None

