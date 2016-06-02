#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import nameparser
nameparser_config = getattr(nameparser, "config")

def suffixes():
	return set(getattr(nameparser_config, 'SUFFIXES', None) or ())

def suffix_acronyms():
	return set(getattr(nameparser_config, 'SUFFIX_ACRONYMS', None) or ())

def suffix_not_acronyms():
	return set(getattr(nameparser_config, 'SUFFIX_NOT_ACRONYMS', None) or ())

def constants():
	suffixes = suffixes() # nameparser 0.3.X
	if suffixes:
		suffixes = suffixes | set(('cfa',))
		constants = nameparser_config.Constants(suffixes=suffixes)
	else:
		suffix_not_acronyms = suffix_not_acronyms()
		suffix_acronyms = suffix_acronyms() | set(('cfa',))
		constants = nameparser_config.Constants(suffix_acronyms=suffix_acronyms,
												suffix_not_acronyms=suffix_not_acronyms)
	return constants
