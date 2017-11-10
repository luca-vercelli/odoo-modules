# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
#import ViewDict ?

import logging
_logger= logging.getLogger(__name__)

_logger.info("mustache_view: Reading class " + __name__)

class TestViewDict(TransactionCase):

	def setUp(self):
		_logger.info("mustache_view: Fucking set up")
		
	def test_normal_dict(self):
		_logger.info("mustache_view: Running test 0 ")
		raise Exception("fuck 0")
		x = ViewDict()
		x['a'] = 12345
		try:
			self.assertEqual(x['a'] , 12345)
		except KeyError:
			self.fail('key "a" not found')
		try:
			y = key['b']
			self.fail('key "b" should not be found')
		except KeyError:
			pass
		self.fail('DEBUG _unknownKeys='+str(x._unknownKeys))

	def test_view_dict(self):
		_logger.info("mustache_view: Running test 1 ")
		raise Exception("fuck 1")
		x = ViewDict()
		try:
			y = x['view_report_invoice_mustache']
			self.faile("DEBUG y="+str(y))
		except KeyError:
			self.fail('key "a" not found')
		self.fail('DEBUG _unknownKeys='+str(x._unknownKeys))
