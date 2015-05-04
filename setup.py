import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
	'console_scripts': [
	],
}

import platform
py_impl = getattr(platform, 'python_implementation', lambda: None)
IS_PYPY = py_impl() == 'PyPy'

TESTS_REQUIRE = [
	'nose',
	'nose2[coverage_plugin]',
	'nose-timer',
	'nose-progressive',
	'nose-pudb',
	'pyhamcrest',
	'zope.container',
	'zope.proxy',
	'zope.testing',
	'nti.nose_traceback_info',
	'nti.testing'
]

setup(
	name='nti.utils',
	version=VERSION,
	author='Jason Madden',
	author_email='jason@nextthought.com',
	description="NTI Utils",
	long_description=codecs.open('README.rst', encoding='utf-8').read(),
	license='Proprietary',
	keywords='utils',
	classifiers=[
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: Implementation :: CPython',
		'Programming Language :: Python :: Implementation :: PyPy'
	],
	packages=find_packages('src'),
	package_dir={'': 'src'},
	namespace_packages=['nti'],
	tests_require=TESTS_REQUIRE,
	install_requires=[
		'setuptools',
		'Acquisition',
		'Babel',
		'ExtensionClass',
		'gevent' if not IS_PYPY else '',
		'greenlet' if not IS_PYPY else '',
		'lingua',
		'numpy' if not IS_PYPY else '',
		'plone.i18n',
		'zope.annotation',
		'zope.component',
		'zope.configuration',
		'zope.deferredimport',
		'zope.deprecation',
		'zope.interface',
		'zope.i18nmessageid',
		'zope.schema',
		'zope.security',
		'zope.vocabularyregistry',
		'nti.common',
		'nti.schema',
		'nti.transactions',
		'pywikipedia'
	],
	extras_require={
		'test': TESTS_REQUIRE,
	},
	dependency_links=[
		'git+https://github.com/NextThought/nti.nose_traceback_info.git#egg=nti.nose_traceback_info'
	],
	entry_points=entry_points
)
