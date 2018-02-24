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

setup(
    name='nti.store',
    version=VERSION,
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI Store",
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
	install_requires=[
		'setuptools'
	],
	entry_points=entry_points
)
