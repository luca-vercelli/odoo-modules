##############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2016 luca Vercelli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models

# see /usr/lib/python2.7/dist-packages/openerp/addons/account/partner.py


class res_partner(models.Model):
    _inherit = "res.partner"

    l10n_it_codice_fiscale_enc = fields.Char(
        string="Codice Fiscale cifrato Sistema TS", copy=False
    )
    opposizione_730 = fields.Boolean("Opposizione alla dichiarazione 730")

    def _encrypt_codice_fiscale(self):
        """
        Encrypt the Italian fiscal code whenever it is changed and saved.
        """
        from . import util

        for record in self:
            if not record.l10n_it_codice_fiscale:
                record.l10n_it_codice_fiscale_enc = None
            else:
                record.l10n_it_codice_fiscale_enc = util.encrypt(
                    record.l10n_it_codice_fiscale
                )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._encrypt_codice_fiscale()
        return records

    def write(self, vals):
        result = super().write(vals)
        if "l10n_it_codice_fiscale" in vals:
            self._encrypt_codice_fiscale()
        return result

    # @api.v8
    def encrypt_all_fiscalcodes(self):
        """
        This encrypts all codice fiscale values on demand.
        """
        from . import util

        model = self.env["res.partner"]
        all_partners = model.search([])
        for record in all_partners:
            if record.l10n_it_codice_fiscale:
                record.l10n_it_codice_fiscale_enc = util.encrypt(
                    record.l10n_it_codice_fiscale
                )
            else:
                record.l10n_it_codice_fiscale_enc = None
