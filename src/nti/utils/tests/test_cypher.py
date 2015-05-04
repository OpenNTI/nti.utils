#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

#disable: accessing protected members, too many methods
#pylint: disable=W0212,R0904

import unittest
from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that

from ..cypher import make_ciphertext, get_plaintext

class TestCypher(unittest.TestCase):

	def test_symmetrical(self):
		text = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
		ciphertext = make_ciphertext(text)
		assert_that(ciphertext, is_not(text))
		plaintext = get_plaintext(ciphertext)
		assert_that(plaintext, is_(text))
