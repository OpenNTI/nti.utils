#!/usr/bin/env python
from __future__ import print_function, unicode_literals

logger = __import__('logging').getLogger(__name__)

import hashlib
import urlparse

import zope.i18nmessageid
MessageFactory = zope.i18nmessageid.MessageFactory('nti.dataserver')


from zope.dottedname import resolve as dottedname

_AVATAR_SERVICES = { 'gravatar': { True: b'secure.gravatar.com',
								   False: b'www.gravatar.com' },
					'libravatar': {True: b'seccdn.libravatar.org',
								   False: b'cdn.libravatar.org'} }

GENERATED_GRAVATAR_TYPES = ('retro', 'identicon', 'monsterid', 'wavatar' )
KNOWN_GRAVATAR_TYPES = GENERATED_GRAVATAR_TYPES + ('mm','404')

def create_gravatar_url( username,
						 defaultGravatarType='mm',
						 secure=False,
						 size=128,
						 service='gravatar'):
	"""
	Return a gravatar URL for the given username (which is assumed to be an email address).

	:keyword basestring defaultGravatarType: The gravatar type to use if no specific
		gravatar is available. Defaults to 'mm' for mystery man.
	:keyword bool secure: If `True` (default `False`) HTTPS URL will be generated.
	:keyword int size: The pixel dimensions of the image, between 1 and 512. Default 128.

	:return: A gravatar URL for the given username. See http://en.gravatar.com/site/implement/images/
	"""
	md5str = hashlib.md5( username.lower() ).hexdigest()

	scheme = b'https' if secure else b'http'
	netloc = _AVATAR_SERVICES[service][secure]
	path = b'/avatar/' + md5str
	params = ''
	query = b's=%s&d=%s' % (size,defaultGravatarType)
	fragment = ''
	return str(urlparse.urlunparse( (scheme,netloc,path,params,query,fragment) ))


import os

def make_cache_dir(cache_name, env_var=None):
	"""
	Global utility to create and return a cache directory in the
	most appropriate position.

	This takes into account environment settings for an active application
	server first. Following that, the python virtual installation is used, and
	finally a system-specific cache location. If all that fails, and the current
	working directory is writable, it will be used.

	:param str cache_name: The specific (filesystem) name of the type of cache
	:param str env_var: If given, then names an environment variable that will be
		queried first. If the environment variable exists, then we will attempt to use
		it in preference to anything else.
	:return: A string giving a path to a directory for the cache.
	:raises ValueError: If no cache location can be found.
	"""

	result = None

	if env_var:
		result = os.environ.get( env_var )

	if result is None:
		# In preference order
		env_child = ( ('DATASERVER_ENV', ('var', 'caches', cache_name)),
					  ('DATASERVER_DIR', ('var', 'caches', cache_name)),
					  ('VIRTUAL_ENV',    ('var', 'caches', cache_name) ) )
		for env_var, child in env_child:
			if env_var in os.environ:
				parent = os.environ[env_var]
				result = os.path.join( parent, *child )
				break

	# Ok, no environment to be found. How about some system specific stuff?
	if result is None:
		for system_loc in ( "~/Library/Caches/", # OS x
							"~/.cache" ): # Linux
			system_loc = os.path.expanduser( system_loc )
			if os.path.isdir( system_loc ):
				result = os.path.join( system_loc, "com.nextthought", "nti.dataserver", cache_name )
				break

	if result is None:
		result = os.path.join( os.getcwd(), '.caches', cache_name )

	try:
		os.makedirs( result )
	except OSError:
		pass

	if not os.path.isdir( result ):
		raise ValueError( "Unable to find cache location for " + cache_name + " using " + result )
	return result

def setupChameleonCache(config=False):
	# Set up a cache for these things to make subsequent renders faster

	result = None
	if not 'CHAMELEON_CACHE' in os.environ or not os.path.isdir( os.path.expanduser( os.environ['CHAMELEON_CACHE'] ) ):
		os.environ['CHAMELEON_CACHE'] = result = make_cache_dir('chameleon_cache')
	else:
		result = os.environ['CHAMELEON_CACHE']

	if config:
		conf_mod = dottedname.resolve('chameleon.config')
		if conf_mod.CACHE_DIRECTORY is None: # previously imported before we set the environment
			conf_mod.CACHE_DIRECTORY = result

	return result
