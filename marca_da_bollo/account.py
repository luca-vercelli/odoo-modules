# -*- encoding: utf-8 -*-
##############################################################################
#
# # Released under GPL v.2
#
##############################################################################

from odoo import models, fields, api


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

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        super(account_invoice,self)._compute_amount()
        print("Marca da bollo. Old amount: " + str(self.amount_total))
        
        try:
            customer = self.partner_id
            if self.type == 'out_invoice' and customer.customer and customer.addebita_marca_da_bollo:
                #out_invoice=it's really an invoice to a customer
                tax = self.env['account.tax'].search([('marca_da_bollo','=',True)])[0]
                #already there? shouldn't be.
                tax_line = sum(1 for line in self.tax_line_ids if line.tax_id.id == tax.id)
                if not tax_line:
                    if self.amount_total > tax.min_for_stamp:
                        self._create_line_marca_da_bollo(tax)
                        super(account_invoice,self)._compute_amount()
                        print("Marca da bollo. Nuovo amount: " + str(self.amount_total))
                    else:
                        print("Marca da bollo non necessaria.")
                else:
                    if self.amount_total <= tax.min_for_stamp:
                        print("Marca da bollo. Dovrei eliminarla, ma probabilmente verrà eliminata in automatico al giro dopo. " + str(self.amount_total))
                    else:
                        print("Marca da bollo già presente.")
                    
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print("Error adding Marca da bollo. Ignored.")

    def _create_line_marca_da_bollo(self, tax):
        currency = self.currency_id.with_context(date=self.date_invoice or fields.Date.context_today(self))
        if not tax.account_id:
            print("Manca il conto sulla marca da bollo!")
            return 
        val = {
                        'invoice_id': self.id,
                        'name': tax.name,
                        'tax_id' : tax.id,
                        'manual': False,
                        'sequence': 999,
                        'base': self.amount_total,
                        'amount': tax.amount,
                        'amount_rounding' : currency.round(0.0),
                        'amount_total' : tax.amount,
                        'account_id' : tax.account_id.id,
                        #'account_analytic_id' : self.account_analytic_id.id,
                    }
        l = self.env['account.invoice.tax'].new(val)


