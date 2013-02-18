#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility classes and objects for working with :mod:`concurrent.futures`.

$Id$
"""

from __future__ import print_function, unicode_literals, absolute_import
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


import functools
import concurrent.futures

def ConcurrentExecutor(max_workers=None, _throw_exceptions=False):
	"""
	An abstraction layer to let code easily switch between different
	concurrency strategies. Import this instead of importing something
	from :mod:`concurrent.futures` directly.

	It also serves as a compatibility shim to make us compatible with
	gevent thread patching. For that reason, we avoid throwing any
	exceptions and instead return them (note: this strategy may
	change); throwing exceptions is not safe in the multiprocessing
	case and can hang the pool, and has undefined results in the
	thread case.
	"""
	# Notice that we did not import the direct class because it gets swizzled at
	# runtime. For that same reason, we subclass dynamically at runtime.
	if _throw_exceptions:
		return concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)

	class _Executor(concurrent.futures.ProcessPoolExecutor):
		# map() channels through submit() so this captures all activity
		def submit( self, fn, *args, **kwargs ):
			_fn = _nothrow(fn)
			_fn = functools.update_wrapper( _fn, fn )
			return super(_Executor,self).submit( _fn, *args, **kwargs )

	return _Executor(max_workers=max_workers)

class _nothrow(object):
	"""
	For submission to executors, a callable that doesn't throw (and avoids hangs.)

	For pickling, must be a top-level object.
	"""
	def __init__(self, fn):
		self.__fn = fn

	def __call__( self, *args, **kwargs):
		try:
			return self.__fn(*args, **kwargs)
		except Exception as e:
			# logging may not be reliable in this pool
			import traceback; traceback.print_exc()
			return e # TODO: These may not be serializable?