# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import account

import logging
_logger = logging.getLogger(__name__)


class ReportAccountInvoice(models.AbstractModel):
    """
    Printing logic
    
    Mako, as qweb, allows us to put logic directly inside report, however we think that's *bad*.
    """
    _name = 'report.view_mako.view_invoice_mako'    #MUST BE: report.<module name>.<report view name (=ID)>

    @api.model
    def render_html(self, docids, data=None):
        report_name = 'view_mako.view_invoice_mako' #MUST BE: <module name>.<report view name (=ID)>
        report_env = self.env['report']
        report = report_env._get_report_from_name(report_name)
        #CHECK data is a dict, isn't it?
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs' : self.env['account.invoice'].browse(docids),
            'report': self,
        }
        
        return report_env.render(report_name, docargs)

    def display_title(self, invoice):
        
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
        return ', '.join(map(lambda x: (x.description or x.name), invoice_line.invoice_line_tax_ids))

    def display_tax_amount_grouped(self, invoice):

        #cfr. _get_tax_amount_by_group()

        map0 = {}
        for line in invoice.tax_line_ids:
            map0.setdefault(line.tax_id.tax_group_id, 0.0)
            map0[line.tax_id.tax_group_id] += line.amount
        list0 = sorted(map0.items(), key=lambda l: l[0].sequence)

        #this line is different from _get_tax_amount_by_group:
        map1 = map(lambda l: { 'name' : l[0].name, 'amount' : l[1]}, list0)

        #FIXME I don't understand this: if len(o.tax_line_ids) > 1 else (o.tax_line_ids.tax_id.description or o.tax_line_ids.tax_id.name)

        return map1

