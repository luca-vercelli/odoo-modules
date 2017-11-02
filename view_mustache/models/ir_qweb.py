# -*- coding: utf-8 -*-

from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

try:
	import pystache
	import re
	import Queue
	import set
except:
	pass

class ViewDict(dict):
	"""
	This dict search keys in the ir.ui.view table, too.
	Keys that are not found are stored in self._unknownKeys for better performance.
	"""
	_unknownKeys = set()

	def __getitem__(self, key):
		if key in self._unknownKeys:
			raise KeyError(key)
		try:
			return super(ViewDict, self).__getitem__(self, key)
		except KeyError:
			view_id = Engine._find_mustache_template(key)
			if view_id is not None:
				self[key] = view_id.arch
				return view_id.arch
			else:
				self._unknownKeys.add(key)
				raise KeyError(key)

	def __putitem__(self, key, value):	
		if key in self._unknownKeys:
			self._unknownKeys.remove(key)
		return super(ViewDict, self).__putitem__(self, key, value)

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
		
		view_id = self._find_mustache_template(id_or_xml_id)
		if view_id is not None:
		
				# only in this case, render using Pystache
				
				templates = self._load_other_templates(view_id.name, view_id.arch)
				if values is None:
					values = {}
				
				values.update(templates)
				
				return pystache.render(view_id.arch, values)	#ignore **options
		
		# In all other cases, render with super()
		return super(Engine, self).render(id_or_xml_id, values, **options)

	def _find_mustache_template(self, id_or_xml_id):
	
		view_id = None
		
		if isinstance(id_or_xml_id, ( int, long ) ):
			view_id = self.env['ir.ui.view'].search([('id', '=', id_or_xml_id)])
			#should check auth...
		elif isinstance(id_or_xml_id, basestring):
			view_id = self.env.ref(id_or_xml_id)
		
		if (view_id is not None) and (len(view_id) == 1) :
			if view_id[0].type and view_id[0].type == "mustache":
				return view_id[0]
		
		return None
		
	def _load_other_templates(self, template_name, template_arch):
		"""
		Find and return all sub-templates that are required by 'template'.
		
		Another possibility is to tell pystache how to find templates ... 
		
		@return dict template names -> template archs
		"""
		
		return {}
		
	#	MATCHER = "{{>[^}]*}}"
	#	all_template_names = [template_name]
	#	all_template_archs = [template_arch]
	#	queue = Queue()
	#	queue.put(template_name)
	#	
	#	while not queue.empty():
	#		try:
	#			cur_template_name = queue.get()
	#			cur_template = self._find_mustache_template(cur_template_name)
	#			if 
	#			
	#			cur_dep_names = re.findall(MATCHER, template)
	#			cur_dep_names = [ dep for dep in cur_deps if dep not in all_templates]
	#			for dep in cur_deps:
	#				view_id = self._find_mustache_template(dep)
	#				
	#				
	#			all_templates.extend(cur_deps)
				

