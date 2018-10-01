# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

try:
	import pystache
	import copy
except:
	pass

class PartialsDict(dict):
	"""
	This dict search keys in the ir.ui.view table, too.
	For each key, the DB is queried only once:
	keys that are found on DB are stored in this dict,
	keys that are not found on DB are stored in self._unknownKeys
	"""
	_unknownKeys = set()

	def __init__(self, engine):
		self.engine = engine
		super(PartialsDict, self).__init__()

	def __getitem__(self, key):
		if key in self._unknownKeys:
			raise KeyError(key)
		try:
			return super(PartialsDict, self).__getitem__(key)
		except KeyError:
			view_arch = self.engine._find_mustache_template(key)
			if view_arch is not None:
				self[key] = view_arch
				return view_arch
			else:
				self._unknownKeys.add(key)
				raise KeyError(key)

	def __putitem__(self, key, value):	
		if key in self._unknownKeys:
			self._unknownKeys.remove(key)
		return super(PartialsDict, self).__putitem__(key, value)
	
	def get(self, key, defaultval=None):
		try:
			return self[key]
		except KeyError:
			return defaultval


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
		
		view_arch = self._find_mustache_template(id_or_xml_id)
		if view_arch is not None:
		
				# only in this case, render using Pystache
				if values is None:
					values = {}
				
				renderer = pystache.Renderer(partials=PartialsDict(self))	#ignore **options
				second_context = Lambdas(renderer)
				return renderer.render(view_arch, values, second_context)
		
		# In all other cases, render with super()
		return super(Engine, self).render(id_or_xml_id, values, **options)

	def _find_mustache_template(self, id_or_xml_id):
		"""
		Return view_id.arch, with some modifications
		"""
		view_id = None
		
		if isinstance(id_or_xml_id, int ):
			view_id = self.env['ir.ui.view'].search([('id', '=', id_or_xml_id)])
			#should check auth...
		elif isinstance(id_or_xml_id, str):
			try:
				view_id = self.env.ref(id_or_xml_id)
			except ValueError:
				raise UserError("Template not found (please use full external ID): " + str(id_or_xml_id))
		
		if (view_id is not None) and (len(view_id) == 1) :
			if view_id[0].type and view_id[0].type == "mustache":
				if not view_id[0].arch:
					return ''
				else:
					return view_id[0].arch.replace("{{&gt;","{{>").replace("<t>","").replace("</t>","")
		
		return None

class Lambdas(object):
	"""
	Pystache does not respect Mustache specs.
	This is the only way I found to make Lambda's work: instead of extending context, I create a new one.
	@see https://stackoverflow.com/questions/47099348 and https://github.com/defunkt/pystache/issues/157
	"""
	def __init__(self, renderer):
		self.renderer = renderer

	def fmt_currency(self):
		def currency(str_amount):
			renderer = self.renderer
			amount = renderer.render(str_amount)
			#FIXME which locale ???
			import locale
			return locale.format("%.2f", float(amount), grouping=True)
		return currency

	def fmt_number(self):
		def number(str_q):
			_logger.info("DEBUG GOING TO RENDER: "+ str(str_q))
			renderer = self.renderer	#deepcopy does not work here
			q = renderer.render(str_q)
			_logger.info("DEBUG RENDERED: "+ str(q))
			#FIXME which locale ???
			try:
				import locale
				return locale.format("%.2g", float(q), grouping=True)
			except:
				return ""
		return number

	def fmt_date(self):
		def date(str_date):
			renderer = self.renderer	#deepcopy does not work here
			date = renderer.render(str_date)
			#FIXME which locale ???
			try:
				return date.strftime('%x')
			except AttributeError:
				# got a string instead of a datetime? Let's hope it's in default format.
				import datetime
				try:
					return datetime.datetime.strptime(str(date),'%Y-%m-%d').strftime('%x')
				except:
					return ""

		return date

	def fmt_time(self):
		def time(str_time):
			renderer = self.renderer	#deepcopy does not work here
			time = renderer.render(str_time)
			#FIXME which locale ???
			try:
				return time.strftime('%X')
			except AttributeError:
				# got a string instead of a datetime? Let's hope it's in default format.
				import datetime
				try:
					return datetime.datetime.strptime(str(time),'%H:%M:%S').strftime('%X')
				except:
					return ""
		return time

	def datetime(self):
		def datetime(str_datetime):
			renderer = self.renderer	#deepcopy does not work here
			datetime = renderer.render(str_datetime)
			#FIXME which locale ???
			try:
				return datetime.strftime('%x %X')
			except AttributeError:
				# got a string instead of a datetime? Let's hope it's in default format.
				import datetime
				try:
					return datetime.datetime.strptime(str(datetime),'%Y-%m-%d %H:%M:%S').strftime('%x %X')
				except:
					return ""
		return datetime

	def b64encode(self):
		def _b64encode(str_data):
			renderer = self.renderer	#deepcopy does not work here
			data = renderer.render(str_data)
			import base64
			try:
				return base64.b64encode(data)
			except TypeError:
				try:
					return base64.b64encode(str(data))
				except:
					return ""
		return _b64encode
