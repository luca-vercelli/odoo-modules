from odoo import tools


def migrate(cr, version):
    """Move values from the old l10n_it_fiscalcode columns when present."""
    if not version or not tools.sql.column_exists(cr, "res_partner", "fiscalcode"):
        return

    cr.execute("""
        UPDATE res_partner
           SET l10n_it_codice_fiscale = fiscalcode
         WHERE COALESCE(l10n_it_codice_fiscale, '') = ''
           AND COALESCE(fiscalcode, '') != ''
    """)
    if tools.sql.column_exists(cr, "res_partner", "fiscalcode_enc"):
        cr.execute("""
            UPDATE res_partner
               SET l10n_it_codice_fiscale_enc = fiscalcode_enc
             WHERE COALESCE(l10n_it_codice_fiscale_enc, '') = ''
               AND COALESCE(fiscalcode_enc, '') != ''
        """)
