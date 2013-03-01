#!/usr/bin/env python

from __future__ import print_function, unicode_literals

from nti.tests import AbstractTestBase
from hamcrest import assert_that, is_

import transaction

try:
	from gevent.queue import Full
	from gevent.queue import Queue
except ImportError:
	from Queue import Full
	from Queue import Queue


from nti.utils.transactions import put_nowait

class PutQueueTest(AbstractTestBase):

	def test_put_succeeds(self):
		queue = Queue() # unbounded
		transaction.begin()

		put_nowait( queue, self )
		# still empty
		assert_that( queue.qsize(), is_( 0 ) )

		transaction.commit()

		assert_that( queue.get(block=False), is_( self ) )

	def test_put_transaction_rollback(self):
		queue = Queue()
		transaction.begin()
		put_nowait( queue, 'aborted' )
		transaction.abort()

		transaction.begin()
		put_nowait( queue, 'committed' )
		transaction.commit()

		assert_that( queue.qsize(), is_( 1 ) )
		assert_that( queue.get( block=False ), is_( 'committed' ) )

	def test_put_multiple_correct_order(self):
		# Early builds had a bug where the sort order of the datamanagers
		# was non-deterministic since it was based on object id, and that's not
		# guaranteed to be atomically increasing. It takes a high iteration count to
		# demonstrate this, though
		queue = Queue()

		for _ in range(10000):
			transaction.begin()

			put_nowait( queue, 'a' )
			put_nowait( queue, 'b' )

			transaction.commit()

			assert_that( queue.get( block=False ), is_( 'a' ) )
			assert_that( queue.get( block=False ), is_( 'b' ) )

	def test_put_failure( self ):
		queue = Queue(1) # unbounded
		queue.put( object() )
		assert_that( queue.qsize(), is_( 1 ) )

		transaction.begin()

		put_nowait( queue, self )
		# still size 1
		assert_that( queue.qsize(), is_( 1 ) )
		with self.assertRaises( Full ) as cm:
			transaction.commit()


		assert_that( cm.exception, is_( Full ) )
		assert_that( queue.get(block=False), is_( object ) )
