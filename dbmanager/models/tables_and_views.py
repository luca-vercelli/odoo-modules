# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class ModelFromView():
	
	def create(self):
		raise UserError("This is a read-only table.")
	def write(self):
		raise UserError("This is a read-only table.")
	def unlink():
		raise UserError("This is a read-only table.")
	
class TablesList(models.Model, ModelFromView):
	_name = "dbmanager.tables"
	_description = "Tables in 'public' schema"
	_table = "dbmanager_tables"
	_auto = False
	
	catalog = fields.Char()
	schema = fields.Char()
	name = fields.Char()
	table_type = fields.Char()
	column_ids = fields.One2many('dbmanager.columns', 'table_id')
			
class ViewsList(models.Model, ModelFromView):
	_name = "dbmanager.views"
	_description = "Views in 'public' schema"
	_table = "dbmanager_views"
	_auto = False
	
	catalog = fields.Char()
	schema = fields.Char()
	name = fields.Char()
	view_definition = fields.Text()
			
class TablesColumns(models.Model, ModelFromView):
	_name = "dbmanager.columns"
	_description = "Table columns in 'public' schema"
	_table = "dbmanager_columns"
	_auto = False
	
	table_catalog = fields.Char()
	table_schema = fields.Char()
	table_name = fields.Char()
	name = fields.Char()
	data_type = fields.Char()
	character_maximum_length = fields.Integer()
	numeric_precision = fields.Integer()
	numeric_scale = fields.Integer()
	table_id = fields.Many2one('dbmanager.tables')
	
