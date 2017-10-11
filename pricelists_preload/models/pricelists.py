# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import product

import logging
_logger = logging.getLogger(__name__)

#Searched attribute
ATTRIBUTE_NAME = "Num."

class Config(models.TransientModel):	#Transient = la tabella viene periodicamente svuotata da un batch
	_inherit = "sale.config.settings"

	default_attr_preload_id = fields.Many2one('product.attribute',
		string='Attribute for Pricelist Preload',
		help="This attribute will appear in Pricelist Preload launch map.",
		default_model='pricelists_preload.run')
	

class PricelistPreloadRun(models.TransientModel):	#Transient = la tabella viene periodicamente svuotata da un batch
	_name = "pricelists_preload.run"
	_description = "Preload pricelist lines"

	#eventuali parametri di lancio
	attr_preload_id = fields.Many2one('product.attribute', string='Attribute')
	qta_id = fields.Many2one(string="Quantità per scatola", comodel_name='product.attribute.value', required=True)

	#azione associata alla pressione del bottone

	@api.one
	def load_now(self):
		"""
		Load pricelist lines for each variant with num = qta_id
		"""

		pricelist_id = self._context.get('active_id', False)

		product_ids = sorted(self.qta_id.product_ids, key=lambda x:x.var_desc)

		if not product_ids:
			pass
			#Give some error message!?! TODO

		pricelist_item_model = self.env['product.pricelist.item']
		for product_id in product_ids:
			row_exists = pricelist_item_model.search([("pricelist_id","=",pricelist_id),("product_id","=",product_id.id)])
			if not row_exists:
				pricelist_item_model.create({
					"pricelist_id" : pricelist_id,
					"applied_on" : '0_product_variant',
					"product_id" : product_id.id,
					"name" : product_id.var_desc,
					"compute_price" : "fixed",
					"fixed_price" : 0.0
					})

# FIXME how to hide / use the two buttons Save/Cancel ?					
#	@api.one
#	def write(self, vals):
#		super(PricelistPreloadRun, self).write(vals)
#		self.load_now()