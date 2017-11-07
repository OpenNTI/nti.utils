#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that

import unittest
from io import BytesIO
from six import StringIO

from nti.utils import babel

from nti.utils.tests import SharedConfiguringTestLayer


class NamedBytesIO(BytesIO):
    name = 'fake'


class NamedStringIO(StringIO):
    name = 'fake'


class TestBabel(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_zcml(self):
        source = b'''\
                <configure i18n_domain="lingua">
                    <dummy title="test title"/>
                </configure>
              '''
        source = NamedBytesIO(source)
        messages = list(babel.extract_zcml(source))
        assert_that(messages, has_length(1))
        assert_that(messages[0], has_length(4))
        assert_that(messages[0][2], is_('test title'))

    def test_xml(self):
        source = u'''<html xmlns:i18n="http://xml.zope.org/namespaces/i18n"
                      i18n:domain="lingua">
                  <dummy i18n:attributes="title" title="tést title"/>
                </html>
                '''.encode('utf-8')
        source = NamedBytesIO(source)
        messages = list(babel.extract_xml(source))
        assert_that(messages, has_length(1))
        assert_that(messages[0], has_length(4))
        assert_that(messages[0][2], is_(u'tést title'))

    def test_python(self):
        source = u'''_(u'Canonical text')'''
        source = NamedStringIO(source)
        messages = list(babel.extract_python(source))
        assert_that(messages, has_length(1))
        assert_that(messages[0], has_length(4))
        assert_that(messages[0][2], is_(u'Canonical text'))
