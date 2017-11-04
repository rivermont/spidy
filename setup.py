from setuptools import setup
from spidy import __version__, __author__, __email__

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md', encoding='utf-8').read()

setup(
    name='spidy-web-crawler',
    version=__version__,
    packages=['spidy'],
    package_data={'spidy': ['config/*', 'docs/*']},
    url='https://github.com/rivermont/spidy',
    license='GPLv3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
    ],
    author=__author__,
    author_email=__email__,
    description='Spidy is the simple, easy to use command line web crawler.',
    long_description=long_description,
    keywords=['crawler', 'web crawler', 'spider', 'web-spider'],
    python_requires='>=3.3',
    entry_points={
        'console_scripts': [
            'spidy=spidy.crawler:main',
        ],
    },
    install_requires=[
        'requests',
        'lxml',
        'flake8',
        'reppy'
    ]
)
