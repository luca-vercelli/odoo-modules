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
 
class ExportRegistry(models.Model):
    _name = 'exportts.export.registry'
    _description = 'Esportazioni TS'

    status = fields.Char('Status', readonly=True)
    date_export = fields.Datetime('Timestamp estrazione', readonly=True)
    date_send = fields.Datetime('Timestamp spedizione', readonly=True)
    xml = fields.Text('XML')
    pdf_filename = fields.Char('File PDF ricevuta', readonly=True)
    csv_filename = fields.Char('File CSV dettaglio errori', readonly=True)
    messages = fields.Text('Messages', readonly=True)


