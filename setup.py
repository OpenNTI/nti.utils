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
    'zope.testing',
    'nti.testing',
    'nti.nose_traceback_info',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        ],
	packages=find_packages('src'),
	package_dir={'': 'src'},
	namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
	install_requires=[
		'setuptools',
        'Acquisition' if not IS_PYPY else '',
        'Babel',
        'ExtensionClass',
        'ZODB',
        'dm.transaction.aborthook',
        'futures',
        'gevent' if not IS_PYPY else '',
        'greenlet' if not IS_PYPY else '', # pypy has its own greenlet implementation
        'lingua',
        'numpy' if not IS_PYPY else '',
        'perfmetrics',
        'plone.i18n',
        'pycrypto' if not IS_PYPY else '',
         # 'scipy' if not IS_PYPY else '', # don't include it yet
        'transaction',
        'z3c.baseregistry',
        'zope.annotation',
        'zope.browserresource',
        'zope.component',
        'zope.configuration',
        'zope.container',
        'zope.deferredimport',
        'zope.deprecation',
        'zope.interface',
        'zope.proxy',
        'zope.schema',
        'zope.vocabularyregistry',
         # nti deps
        'nti.common',
        'nti.schema',
        'pywikipedia',
	],
    dependency_links=[
        'git+https://github.com/NextThought/nti.schema.git#egg=nti.schema',
        'git+https://github.com/NextThought/nti.nose_traceback_info.git#egg=nti.nose_traceback_info'
    ],
	entry_points=entry_points
)
