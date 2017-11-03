# -*- coding: utf-8 -*-

from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

try:
	import pystache
	import set
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
	
	
		_logger.warn("SONO QUA!!! key=" + str(key))
		
		
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
				self._extend_values(values)
				
				renderer = pystache.Renderer(partials=PartialsDict(self))	#ignore **options
				return renderer.render(view_arch, values)
		
		# In all other cases, render with super()
		return super(Engine, self).render(id_or_xml_id, values, **options)

	def _find_mustache_template(self, id_or_xml_id):
		"""
		Return view_id.arch, with some modifications
		"""
		view_id = None
		
		if isinstance(id_or_xml_id, ( int, long ) ):
			view_id = self.env['ir.ui.view'].search([('id', '=', id_or_xml_id)])
			#should check auth...
		elif isinstance(id_or_xml_id, basestring):
			view_id = self.env.ref(id_or_xml_id)
		
		if (view_id is not None) and (len(view_id) == 1) :
			if view_id[0].type and view_id[0].type == "mustache":
				if not view_id[0].arch:
					return ''
				else:
					return view_id[0].arch.replace("{{&gt;","{{>").replace("<t>","").replace("</t>","")
		
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
			return locale.format("%.2f", float(amount), grouping=True)
		values['fmt_currency'] = currency

		def number(q):
			#FIXME which locale ???
			import locale
			return locale.format("%.2g", float(q), grouping=True)
		values['fmt_number'] = number

		def date(date):
			#FIXME which locale ???
			try:
				return date.strftime('%x')
			except AttributeError:
				# got a string instead of a datetime? Let's hope it's in default format.
				import datetime
				return datetime.datetime.strptime(str(date),'%Y-%m-%d').strftime('%x')
		values['fmt_date'] = date

		def time(time):
			#FIXME which locale ???
			try:
				return time.strftime('%X')
			except AttributeError:
				# got a string instead of a datetime? Let's hope it's in default format.
				import datetime
				return datetime.datetime.strptime(str(time),'%H:%M:%S').strftime('%X')
		values['fmt_time'] = time

		def datetime(datetime):
			#FIXME which locale ???
			try:
				return datetime.strftime('%x %X')
			except AttributeError:
				# got a string instead of a datetime? Let's hope it's in default format.
				import datetime
				return datetime.datetime.strptime(str(datetime),'%Y-%m-%d %H:%M:%S').strftime('%x %X')
		values['fm_datetime'] = datetime

		def b64encode(data):
			import base64
			return base64.b64encode(data)
		values['fmt_b64encode'] = b64encode
		