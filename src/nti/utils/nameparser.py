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
version_info = getattr(nameparser, 'VERSION', (0, 3, 16))

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
	prefixes = all_prefixes() if not prefixes else prefixes
	extra_suffixes = () if not extra_suffixes else extra_suffixes
	if version_info[0] == 0 and version_info[1] <= 3: # nameparser 0.3.X
		v3_suffixes = suffixes() | set(extra_suffixes)
		constants = nameparser_config.Constants(prefixes=prefixes, suffixes=v3_suffixes)
	else:
		not_acronyms = suffix_not_acronyms()
		acronyms = suffix_acronyms() | set(extra_suffixes)
		constants = nameparser_config.Constants(prefixes=prefixes,
												suffix_acronyms=acronyms,
												suffix_not_acronyms=not_acronyms)
	return constants