# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

try:
	from mako.template import Template
except:
	pass

#see base/ir/ir_qweb/ir_qweb.py
class Engine(models.AbstractModel):
	"""
	Mustache rendering engine
	"""
	_inherit = 'ir.qweb'

	@api.model
	def render(self, id_or_xml_id, values=None, **options):
		""" render(id_or_xml_id, values, **options)

		Render the template specified by the given name.

		:param id_or_xml_id: name or etree (see get_template)
		:param dict values: template values to be used for rendering
		:param options: used to compile the template (the dict available for the rendering is frozen)
			* ``load`` (function) overrides the load method
			* ``profile`` (float) profile the rendering (use astor lib) (filter
			  profile line with time ms >= profile)
		"""
		
		view_id = self._find_mako_template(id_or_xml_id)
		if view_id is not None:
		
				# only in this case, render using Mako
				
				if values is None:
					values = {}
				self._extend_values(values)

				tpl = Template(view_id.arch)
				return tpl.render(**values)	#ignore **options
		
		# In all other cases, render with super()
		return super(Engine, self).render(id_or_xml_id, values, **options)

	def _find_mako_template(self, id_or_xml_id):
	
		view_id = None
		
		if isinstance(id_or_xml_id, ( int, long ) ):
			view_id = self.env['ir.ui.view'].search([('id', '=', id_or_xml_id)])
			#should check auth...
		elif isinstance(id_or_xml_id, basestring):
			view_id = self.env.ref(id_or_xml_id)
		
		if (view_id is not None) and (len(view_id) == 1) :
			if view_id[0].type and view_id[0].type == "mako":
				return view_id[0]
		
		return None
		
	def _extend_values(self, values):
		"""
		Extend values with interesting functions.
		@param values must be a dict, not None.
		"""
		engine = self

		def currency(amount):
			#FIXME which locale ???
			import locale
			return locale.format("%.2f", amount, grouping=True)
		values['currency'] = currency

		def number(q):
			#FIXME which locale ???
			import locale
			return locale.format("%.2g", q, grouping=True)
		values['number'] = currency

		def date(date):
			#FIXME which locale ???
			try:
				return date.strftime('%x')
			except AttributeError:
				# got a string instead of a datetime? Let's hope it's in default format.
				import datetime
				return datetime.datetime.strptime(str(date),'%Y-%m-%d').strftime('%x')
		values['date'] = date

		def time(time):
			#FIXME which locale ???
			try:
				return time.strftime('%X')
			except AttributeError:
				# got a string instead of a datetime? Let's hope it's in default format.
				import datetime
				return datetime.datetime.strptime(str(time),'%H:%M:%S').strftime('%X')
		values['time'] = time

		def datetime(datetime):
			#FIXME which locale ???
			try:
				return datetime.strftime('%x %X')
			except AttributeError:
				# got a string instead of a datetime? Let's hope it's in default format.
				import datetime
				return datetime.datetime.strptime(str(datetime),'%Y-%m-%d %H:%M:%S').strftime('%x %X')
		values['datetime'] = datetime

		def render(template_external_id, **more_values):
			try:
				view_id = engine._find_mako_template(template_external_id)
			except ValueError:
				view_id = None
			if not view_id:
				raise UserError("Template not found (please use external ID): " + str(template_external_id))
			from mako.template import Template
			tpl = Template(view_id.arch)
			tpl_values = dict(values)	#Clone dict, then update it
			tpl_values.update(more_values)
			rendered = tpl.render(**tpl_values)
			
			_logger.info ("SONO QUI E rendered="+str(rendered))	#DEBUG CODE
			
			return rendered
		values['render'] = render

		def b64encode(data):			# DOES NOT WORK
			import base64
			return base64.b64encode(data)
		values['b64encode'] = b64encode


