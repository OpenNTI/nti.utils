#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import has_entry
from hamcrest import assert_that
from hamcrest import has_property

import unittest

from zope import interface
from zope.annotation import interfaces as an_interfaces

from nti.utils.property import annotation_alias

class TestProperty(unittest.TestCase):
	
	def test_annotation_alias(self):
	
		@interface.implementer(an_interfaces.IAnnotations)
		class X(dict):
			the_alias = annotation_alias( 'the.key', delete=True, default=1 )
	
		x = X()
		# Default value
		assert_that( x, has_property( 'the_alias', 1 ) )
	
		# Set
		x.the_alias = 2
		assert_that( x, has_property( 'the_alias', 2 ) )
		assert_that( x, has_entry( 'the.key', 2 ) )
	
		# del
		del x.the_alias
		assert_that( x, has_property( 'the_alias', 1 ) )
	
		# quiet re-del
		del x.the_alias
		assert_that( x, has_property( 'the_alias', 1 ) )
