#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various python3/pypy compatibility shims.

$Id$
"""

from __future__ import print_function, unicode_literals, absolute_import
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

try:
	from Acquisition.interfaces import IAcquirer
except ImportError:
	class IAcquirer(interface.Interface):
		pass

try:
	from Acquisition import Implicit
except ImportError:
	@interface.implementer(IAcquirer)
	class Implicit(object):
		pass

try:
	from ExtensionClass import Base
except ImportError:
	class Base(object):
		pass

try:
	from Acquisition import aq_base
except ImportError: # pypy?
	def aq_base( o ):
		return o