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

 
class ExportRegistry(models.Model):
    _name = 'exportts.export.registry'
    _description = 'Esportazioni TS'

    date_run = fields.Date('Mese')
    status = fields.Char(readonly=True)
    xml_filename = fields.Char(readonly=True)
    pdf_filename = fields.Char(readonly=True)
    csv_filename = fields.Char(readonly=True)

    
    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        obj = super(ExportRegistry, self).create(vals)
        obj.fix_date()
        #obj.export()
        return obj

    @api.one
    def fix_date(self):
        import datetime, calendar
        #date_run_dt = datetime.date.fromisoformat(self.date_run)
        date_run_dt = datetime.datetime.strptime(self.date_run,"%Y-%m-%d")
        last_day_of_month = calendar.monthrange(date_run_dt.year, date_run_dt.month)[1]
        self.date_run = fields.Date.from_string(str(date_run_dt.year)+"-"+str(date_run_dt.month)+"-"+str(last_day_of_month))

    @api.one
    def export(self):

        filename = 'export-ts-' + date.strftime('YYYY-MM-DD', self.date_run) + '.xml'
        #TODO EXPORT TO file
        
        self.write({
            xml_filename : filename,
            status : 'Exported'
            })

