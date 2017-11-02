# -*- coding: utf-8 -*-

from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)


class View(models.Model):
	"""
	Add a new selection "Mako" in view types
	"""
	_inherit = "ir.ui.view"

	type = fields.Selection(selection_add=[('mako','Mako')])

