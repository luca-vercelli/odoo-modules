# -*- coding: utf-8 -*-

from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class ReportAccountInvoice(models.AbstractModel):
    _name = 'report.view_mustache.view_invoice_mustache'    #MUST BE: report.<module name>.<report view name (=ID)>
    
    @api.model
    def render_html(self, docids, data=None):
        report_name = 'view_mustache.view_invoice_mustache' #MUST BE: <module name>.<report view name (=ID)>
        report_env = self.env['report']
        report = report_env._get_report_from_name(report_name)
        
        docs = self.env['account.invoice'].browse(docids)
        
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs' : docs,         #self.env['account.invoice'].browse(docids),
            'company': self.env.user.company_id        # needed by hewader / footer partials
        }
        
        _logger.info("HERE docargs="+str(docargs))

        return report_env.render(report_name, docargs)

class AccountInvoice(models.Model):
    """
    Printing logic
    """
    _inherit = 'account.invoice'

    display_title = fields.Char('Display title', compute='_display_title')
    @api.depends('type','state')
    def _display_title(self):
        for invoice in self:
            if invoice.type == 'out_invoice':
                #FIXME is there some kind of "switch" in Python?
                if invoice.state == 'open' or invoice.state == 'paid':
                    invoice.display_title = "Invoice"
                elif invoice.state == 'proforma2':
                    invoice.display_title = "PRO-FORMA"
                elif invoice.state == 'draft':
                    invoice.display_title = "Draft Invoice"
                elif invoice.state == 'cancel':
                    invoice.display_title = "Cancelled Invoice"
            elif invoice.type == 'in_refund':
                invoice.display_title = "Vendor Refund"
            elif invoice.type == 'in_invoice':
               invoice.display_title = "Vendor Invoice"
            else:
                invoice.display_title = None

    display_date_due = fields.Boolean('Display date due', compute='_display_date_due')
    @api.depends('type','state', 'date_due')
    def _display_date_due(self):
        for invoice in self:
            invoice.display_date_due = invoice.date_due and invoice.type == 'out_invoice' and (invoice.state == 'open' or invoice.state == 'paid')

    display_discount = fields.Boolean('Display discount', compute='_display_discount')
    @api.depends('invoice_line_ids')
    def _display_discount(self):
        for invoice in self:
            invoice.display_discount = any([l.discount for l in invoice.invoice_line_ids])

    #FIXME this is not working
    display_tax_amount_grouped = fields.One2many('Display taxes table',compute='_display_tax_amount_grouped')
    @api.depends('tax_line_ids')
    @api.one
    def _display_tax_amount_grouped(self):
        #cfr. _get_tax_amount_by_group()

        invoice = self

        map0 = {}
        for line in invoice.tax_line_ids:
            map0.setdefault(line.tax_id.tax_group_id, 0.0)
            map0[line.tax_id.tax_group_id] += line.amount
        list0 = sorted(map0.items(), key=lambda l: l[0].sequence)

        #this line is different from _get_tax_amount_by_group:
        map1 = map(lambda l: { 'name' : l[0].name, 'amount' : l[1]}, list0)

        #FIXME I don't understand this: if len(o.tax_line_ids) > 1 else (o.tax_line_ids.tax_id.description or o.tax_line_ids.tax_id.name)

        return map1

class AccountInvoiceLine(models.Model):
    """
    Printing logic
    """
    _inherit = 'account.invoice.line'

    display_taxes = fields.Char('Display taxes', compute='_display_taxes')
    @api.depends('invoice_line_tax_ids')
    def display_taxes(self):
        for invoice_line in self:
            invoice_line.display_taxes = ', '.join(map(lambda x: (x.description or x.name), invoice_line.invoice_line_tax_ids))


