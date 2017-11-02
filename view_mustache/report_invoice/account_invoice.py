# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import account

import logging
_logger = logging.getLogger(__name__)

try:
	import pystache
except:
	pass
	

class ReportAccountInvoice(models.AbstractModel):
	"""
	Printing logic
	"""
	_name = 'report.view_mustache.report_invoice_mustache'

	@api.model
	def render_html(self, docids, data=None):
		report_name = 'view_mustache.report_invoice_mustache'
		report_env = self.env['report']
		report = report_env._get_report_from_name(report_name)
		docargs = {
			'doc_ids': docids,
			'doc_model': report.model,
			'docs': self,
			'display_title': self.display_title,
		}
		
		_logger.info("SONO QUI E report="+str(report)) #DEBUG
		
		return report_env.render(report_name, docargs)

	def display_title(self):
		
		_logger.info("SONO QUI! e self=" + str(self))	#DEBUG
	
	
		if self.type == 'out_invoice':
			#FIXME is there some kind of "switch" in Python?
			if self.state == 'open' or self.state == 'paid':
				return "Invoice"
			elif self.state == 'proforma2':
				return "PRO-FORMA"
			elif self.state == 'draft':
				return "Draft Invoice"
			elif self.state == 'cancel':
				return "Cancelled Invoice"
		elif self.type == 'in_refund':
			return "Vendor Refund"
		elif self.type == 'in_invoice':
			return "Vendor Invoice"
		else:
			return None

	#FIXME function or computed field?
	def display_due_date(self, invoice):
		return invoice.date_due and invoice.type == 'out_invoice' and (invoice.state == 'open' or invoice.state == 'paid')

	def display_discount(self, invoice):
		return any([l.discount for l in invoice.invoice_line_ids])

	def display_taxes(self, invoice_line):
		return ', '.join(map(lambda x: (x.description or x.name), invoice_line.invoice_line_tax_ids))

	def display_tax_amount_grouped(self, invoice):

		#cfr. _get_tax_amount_by_group()

		map0 = {}
		currency = invoice_line.currency_id or invoice_line.company_id.currency_id
		for line in invoice_line.tax_line_ids:
			map0.setdefault(line.tax_id.tax_group_id, 0.0)
			map0[line.tax_id.tax_group_id] += line.amount
		list0 = sorted(map0.items(), key=lambda l: l[0].sequence)

		#this line is different from _get_tax_amount_by_group:
		map1 = map(lambda l: { 'name' : l[0].name, 'amount' : l[1]}, list0)

		#FIXME I don't understand this: if len(o.tax_line_ids) > 1 else (o.tax_line_ids.tax_id.description or o.tax_line_ids.tax_id.name)

		return map1

