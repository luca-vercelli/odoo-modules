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

 
class exportts_config(models.Model):
    _name = 'exportts.run.registry'
    _description = 'Run'

    date = fields.Date('Last day of month of run')
    status = fields.Char()
    xml = fields.Char()

class exportts_run_registry(models.Model):
    _name = 'exportts.run.registry'
    _description = 'Run'

    date = fields.Date('Last day of month of run')
    status = fields.Char()
    xml = fields.Char()

class exportts_export(models.TransientModel):n
	_name = "exportts.export"
	_description = "Estrai fatture in XML"

	@api.one
	def do_smthg(self):
        pass

class exportts_export(models.TransientModel):
	_name = "exportts.send"
	_description = "Invia XML a Sistema TS"

	@api.one
	def do_smthg(self):
        pass


