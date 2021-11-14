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

    name = fields.Char('Nome', compute='_compute_name')
    status = fields.Char('Status', readonly=True)
    proprietario_id = fields.Many2one('res.partner',string='Proprietario')
    date_export = fields.Datetime('Timestamp estrazione', readonly=True)
    date_send = fields.Datetime('Timestamp spedizione', readonly=True)
    xml = fields.Text('XML')
    pdf_filename = fields.Char('File PDF ricevuta', readonly=True)
    csv_filename = fields.Char('File CSV dettaglio errori', readonly=True)
    messages = fields.Text('Messages', readonly=True)
    pdf_link = fields.Char('Download receipt', compute='_compute_pdf_link')
    csv_link = fields.Char('Download error details', compute='_compute_csv_link')
    
    @api.multi
    def _compute_name(self):
        for rec in self:
            rec.name = str(rec.date_export)

    @api.depends('pdf_filename')
    def _compute_pdf_link(self):
        for record in self:
            record.pdf_link = '/web/sistemats/receipt/' + str(record.id)

    @api.depends('csv_filename')
    def _compute_csv_link(self):
        for record in self:
            record.csv_link = '/web/sistemats/errors/' + str(record.id)
