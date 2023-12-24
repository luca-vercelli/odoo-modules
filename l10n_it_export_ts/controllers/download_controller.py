# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2021 luca Vercelli
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

from odoo import models, fields, api
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition
#from odoo.addons.web.controllers.main import serialize_exception
from werkzeug.datastructures import Headers


class DownloadSistemaTsAttachments(http.Controller):
    # see https://stackoverflow.com/questions/38120510

    @http.route('/web/sistemats/receipt/<int:id>', type='http', auth="public")
    #@serialize_exception
    def download_receipt(self, id, **kw):
        """ let the user download pdf_filename """
        export = request.env['exportts.export.registry'].browse(id)
        if not export or not export.pdf_filename:
            return request.not_found("Report not available")
        else:
            return self.common_make_response(export.pdf_filename, "application/pdf")

    @http.route('/web/sistemats/errors/<int:id>', type='http', auth="public")
    #@serialize_exception
    def download_errors(self, id, **kw):
        """ let the user download csv_filename """
        export = request.env['exportts.export.registry'].browse(id)
        if not export or not export.csv_filename:
            return request.not_found("Report not available")
        else:
            return self.common_make_response(export.csv_filename, "application/x-zip")

    def common_make_response(self, filepath, mimeType):
        filename = self.get_filename(filepath)
        with open(filepath, 'rb') as f:
            file_content = f.read()
        headers = Headers()
        headers.add('Content-Type', mimeType)
        headers.add('Content-Disposition', 'attachment', filename=filename)
        return request.make_response(file_content, headers)

    def get_filename(self, filepath):
        """ /a/b/c   ->   c """
        if not filepath:
            return filepath
        if '/' not in filepath:
            return filepath
        return filepath[filepath.rindex('/')+1:]
