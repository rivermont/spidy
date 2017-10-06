from setuptools import setup
from spidy import __version__, __author__, __email__

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='spidy',
    version=__version__,
    packages=['spidy'],
    package_data={'spidy': ['config/*', 'media/*']},
    url='https://github.com/rivermont/spidy',
    license='GPLv3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP'
    ],
    author=__author__,
    author_email=__email__,
    description='Spidy is the simple, easy to use command line web crawler.',
    long_description=readme,
    keywords=["spider", "web crawler", "scraping"],
    python_requires='>=3.3',
    entry_points={
        'console_scripts': [
            'spidy=spidy.crawler:main',
        ],
    },
    install_requires=[
        'requests',
        'lxml',
        'flake8'
    ]
)
