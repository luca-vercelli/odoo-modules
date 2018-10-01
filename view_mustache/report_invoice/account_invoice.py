# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import account

import logging
_logger = logging.getLogger(__name__)

class FakeDict(dict):
    def __init__(self, orig_dict={}):
        super(FakeDict, self).__init__(orig_dict)
    
    def __getitem__(self, key):
        try:
            return super(FakeDict, self).__getitem__(key)
        except KeyError:
            if self.__hasattr__(key):
                return self.display_title()    #FIXME ma con che contesto????
            else:
                raise KeyError(key)
    
    def display_title(self, invoice):
        
        _logger.info("QUI STO LEGGENDO display_title dal dict")
        
        return "TODO"
    
    
class ReportAccountInvoice(models.AbstractModel):
    """
    Printing logic
    
    Extend invoice with missing attributes.
    
    Format all fields as required...
    
    """
    _name = 'report.view_mustache.view_invoice_mustache'    #MUST BE: report.<module name>.<report view name (=ID)>
    
    @api.model
    def render_html(self, docids, data=None):
        report_name = 'view_mustache.view_invoice_mustache' #MUST BE: <module name>.<report view name (=ID)>
        report_env = self.env['report']
        report = report_env._get_report_from_name(report_name)
        
        orig_docs = self.env['account.invoice'].browse(docids)
        docs = []
        
        #import pdb
        #pdb.set_trace()

        for doc in orig_docs:
            #avoid undesired DB updates
            doc.write = lambda self,data: self
            
            #doc.number = (doc.number or '')	#errore col lambda nel __set__
            doc.display_title = self.display_title(doc)
            doc.display_date_due = self.display_date_due(doc)
            doc.display_discount = self.display_discount(doc)
            doc.display_tax_amount_grouped = self.display_tax_amount_grouped(doc)
            #doc_line.display_taxes = self.display_taxes(doc_line)
            docs.append(doc)
        
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs' : docs,         #self.env['account.invoice'].browse(docids),
            'company': self.env.user.company_id        # needed by hewader / footer partials
        }
        
        return report_env.render(report_name, docargs)

    def display_title(self, invoice):
        
        _logger.info("QUI STO LEGGENDO _display_title")

        if invoice.type == 'out_invoice':
            #FIXME is there some kind of "switch" in Python?
            if invoice.state == 'open' or invoice.state == 'paid':
                return "Invoice"
            elif invoice.state == 'proforma2':
                return "PRO-FORMA"
            elif invoice.state == 'draft':
                return "Draft Invoice"
            elif invoice.state == 'cancel':
                return "Cancelled Invoice"
        elif invoice.type == 'in_refund':
            return "Vendor Refund"
        elif invoice.type == 'in_invoice':
            return "Vendor Invoice"
        else:
            return None

    #FIXME function or computed field?
    def display_date_due(self, invoice):
        return invoice.date_due and invoice.type == 'out_invoice' and (invoice.state == 'open' or invoice.state == 'paid')

    def display_discount(self, invoice):
        return any([l.discount for l in invoice.invoice_line_ids])

    def display_taxes(self, invoice_line):
        return ', '.join([(x.description or x.name) for x in invoice_line.invoice_line_tax_ids])

    def display_tax_amount_grouped(self, invoice):

        #cfr. _get_tax_amount_by_group()

        map0 = {}
        for line in invoice.tax_line_ids:
            map0.setdefault(line.tax_id.tax_group_id, 0.0)
            map0[line.tax_id.tax_group_id] += line.amount
        list0 = sorted(list(map0.items()), key=lambda l: l[0].sequence)

        #this line is different from _get_tax_amount_by_group:
        map1 = [{ 'name' : l[0].name, 'amount' : l[1]} for l in list0]

        #FIXME I don't understand this: if len(o.tax_line_ids) > 1 else (o.tax_line_ids.tax_id.description or o.tax_line_ids.tax_id.name)

        return map1

