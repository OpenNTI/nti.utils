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

def all_prefixes():
	return set(getattr(nameparser_config, 'PREFIXES', None) or ())

def all_suffixes():
	return suffixes() | suffix_acronyms() | suffix_not_acronyms()

def constants(prefixes=(), extra_suffixes=()):
	v3_suffixes = suffixes()  # nameparser 0.3.X
	prefixes = all_prefixes() if not prefixes else prefixes
	extra_suffixes = () if not extra_suffixes else extra_suffixes
	if v3_suffixes:  # nameparser 0.3.X
		v3_suffixes = v3_suffixes | set(extra_suffixes)
		constants = nameparser_config.Constants(prefixes=prefixes, suffixes=v3_suffixes)
	else:
		suffix_not_acronyms = suffix_not_acronyms()
		suffix_acronyms = suffix_acronyms() | set(extra_suffixes)
		constants = nameparser_config.Constants(prefixes=prefixes,
												suffix_acronyms=suffix_acronyms,
												suffix_not_acronyms=suffix_not_acronyms)
	return constants
