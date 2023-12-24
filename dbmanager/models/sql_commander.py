# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

def format_select_html(rows, field_names, callback=None):
	"""
	Take a table and format it in HTML
	@param rows
		list of lists
	@param field_names
		list of strings
	@return
		single big string containing HTML data
	"""
	outbuffer = '<table class="o_list_view table table-condensed table-striped">\r\n'
	outbuffer += '<thead>\r\n'
	for name in field_names:
		outbuffer += '<th>%s</th>\r\n' % str(name)
	outbuffer += '</thead>\r\n'
	outbuffer += '<tbody>\r\n'
	for row in rows:
		if callback is None:
			outbuffer += '<tr>'
		else:
			outbuffer += '<tr onclick="javascript:alert(''%s'')">' % callback
		for cell in row:
			outbuffer += '<td>%s</td>' % str(cell)
		outbuffer += '</tr>\r\n'
	outbuffer += '</tbody>\r\n'
	outbuffer += '</table>\r\n'
	return outbuffer

def execute_and_format_select_html(cursor, query, callback=None):
	"""
	Execute a SELECT statement, then call format_select_html()
	"""
	_logger.info("Executing: " + query)
	cursor.execute(query)
	rows = cursor.fetchall()
	field_names = [x[0] for x in cursor.description]
	return format_select_html(rows, field_names, callback)


def _compute_command_output(self):
	"""
	Utility method for classes that execute and show a single command
	"""
	return execute_and_format_select_html(self._cr, self.command)

class SqlCommander(models.TransientModel):	#Transient = table periodically made empty by a batch
	_name = "dbmanager.sql.commander"
	_description = "Executor of SQL commands"

	command = fields.Text('SQL Command', help="Type any SQL command (SELECT/INSERT/UPDATE/...) here. The command will be executed on current database.")
	command_output = fields.Html('Command output', readonly=True)

	#@api.one
	def execute(self):
		"""
		Button pressed
		"""
		_logger.info("Executing: " + self.command)
		
		cursor = self._cr
		cursor.execute(self.command)
		rowcount = cursor.rowcount
		try:
			# is this a SELECT?
			rows = cursor.fetchall()
		except:
			# No, probably it is not
			self.command_output = "%d rows affected." % rowcount
			return
		
		field_names = [x[0] for x in cursor.description]
		self.command_output = format_select_html(rows, field_names)
		
