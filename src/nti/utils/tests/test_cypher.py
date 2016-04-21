#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that

import unittest

from nti.utils.cypher import get_plaintext
from nti.utils.cypher import make_ciphertext

class TestCypher(unittest.TestCase):

	def test_symmetrical(self):
		text = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
		ciphertext = make_ciphertext(text)
		assert_that(ciphertext, is_not(text))
		plaintext = get_plaintext(ciphertext)
		assert_that(plaintext, is_(text))
