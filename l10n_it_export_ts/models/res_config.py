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

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    #TODO i default potrebbero essere presi dall'azienda
     
    default_cf_proprietario = fields.Char('C.F. Proprietario', default_model='exportts.wizard.send')
    default_pi_proprietario = fields.Char('P.IVA Proprietario', default_model='exportts.wizard.send')
    default_pincode_inviante = fields.Integer('PINCODE inviante', default_model='exportts.wizard.send')
    default_password_inviante = fields.Char('Password', default_model='exportts.wizard.send')
    default_url = fields.Char('URL', default='http://example.com', default_model='exportts.wizard.send')
    
