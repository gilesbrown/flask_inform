"""
Flask-Inform
------------

A Flask library for generating Inform self-describing ReSTful web services.
"""
from setuptools import setup


setup(
    name='Flask-Inform',
    version='0.1',
    #url='http://example.com/flask-sqlite3/',
    license='BSD',
    author='Giles Brown',
    author_email='gilessbrown@gmail.com',
    description='Very short description',
    long_description=__doc__,
    #py_modules=['flask_inform'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    packages=['flask_inform'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
