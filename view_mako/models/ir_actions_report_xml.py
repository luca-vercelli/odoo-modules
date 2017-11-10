# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ir_actions_report(models.Model):
	_inherit = 'ir.actions.report.xml'

	def allowed_associated_view_types(self):
		"""
		Return list of view types allowed for association with reports (e.g. 'qweb', 'mako', 'mustache', ...)
		"""
		try:
			viewtypes = super(ir_actions_report, self).allowed_associated_view_types()
		except AttributeError:
			#you can install view_mustache and/or view_mako in the order you want
			viewtypes = []
		viewtypes.extend(['qweb', 'mako'])
		return viewtypes
	
	@api.multi
	def associated_view(self):
		"""
		Override to include "Mako" type
		
		Unluckily, I had to completely override this method, without calling super().
		"""
		self.ensure_one()
		action_ref = self.env.ref('base.action_ui_view')
		if not action_ref or len(self.report_name.split('.')) < 2:
			return False
		action_data = action_ref.read()[0]
		
		action_data['domain'] = [('name', 'ilike', self.report_name.split('.')[1]), ('type', 'in', self.allowed_associated_view_types())]
		return action_data
