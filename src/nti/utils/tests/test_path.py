#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import unittest

from nti.utils.path import caller_name

def B(skip=1):
    return caller_name(skip=skip)

def A(skip=1):
    return B(skip=skip)
        
class TestPath(unittest.TestCase):
    
    def test_caller_name(self):
        assert_that(A(1), is_('nti.utils.tests.test_path.B'))
        assert_that(A(2), is_('nti.utils.tests.test_path.A'))
        assert_that(A(3), is_('nti.utils.tests.test_path.TestPath.test_caller_name'))