# -*- encoding: utf-8 -*-
##############################################################################
#
# # Released under GPL v.2
#
##############################################################################

from openerp import models, fields, api


class partner(models.Model):
    _inherit = 'res.partner'
    
    addebita_marca_da_bollo = fields.Boolean('Addebita Marca da Bollo')
    
    _defaults = {
        'addebita_marca_da_bollo': True,
    }

class account_tax(models.Model):
    _inherit = 'account.tax'
    
    #this field is readonly and default False. If you delete the unique tax "Marca da bollo", you get fucked.
    marca_da_bollo = fields.Boolean('Marca da bollo', help="This is the tax used as 'Marca da bollo'.", readonly=True)
    min_for_stamp = fields.Float('Minimo per marca da bollo', help="La marca sarà addebitata se l'imponibile è superiore a questo valore.")
    
    _defaults = {
        'min_for_stamp': 77.48,
        'marca_da_bollo': False,
    }
    
class account_invoice_tax(models.Model):
    """
    La fattura è composta di testata, righe articolo, e righe di tasse (queste)
    """
    _inherit = 'account.invoice.tax'
    
    def compute(self, invoice):
        """
        Questa routine viene richiamata per ricalcolare tutte le righe di tassa
        Le righe di tassa sono raggruppate secondo i 3 conti economici (account_id, base_code_id, tax_code_id),
        il che è per noi molto buffo. Sono tentato di dichiararle come tasse "manuali", ma non verrebbero mai cancellate.
        """
        tax_grouped = super(account_invoice_tax,self).compute(invoice)
        
        #return tax_grouped #DEBUG disable module
        
        try:
            customer = invoice.partner_id
            if invoice.type == 'out_invoice' and customer.customer and customer.addebita_marca_da_bollo:
                #out_invoice= è davvero una fattura,non una nota di credito o altro
                tax = self.env['account.tax'].search([('marca_da_bollo','=',True)])[0]
                prev_amount = sum([v['amount'] for v in tax_grouped.values()]) or 0
                if prev_amount + invoice.amount_untaxed > tax.min_for_stamp:
                    currency = invoice.currency_id.with_context(date=invoice.date_invoice or fields.Date.context_today(invoice))
                    key = (tax.tax_code_id.id or 0, tax.base_code_id.id or 0, tax.account_collected_id.id or invoice.account_id.id)
                    
                    print "DEBUG", key
                    val = {
                        'invoice_id': invoice.id,
                        'name': tax.name,    
                        'amount': tax.amount,
                        'manual': False,
                        'sequence': tax.sequence,
                        'base': prev_amount + invoice.amount_untaxed,
                        'base_code_id' : tax.base_code_id,
                        'tax_code_id' : tax.tax_code_id,
                        'base_amount' : currency.round(0.0),
                        'tax_amount' : currency.round(tax.amount),
                        'account_id' : tax.account_collected_id.id or invoice.account_id.id,
                        'account_analytic_id' : tax.account_analytic_collected_id.id,
                    }
                    tax_grouped[key] = val
        except:
            print "Error adding Marca da bollo. Ignored."
        return tax_grouped
        
