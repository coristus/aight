"""A prototyping framework for ... .
See:
https://github.com/jcgronde/e5
"""
import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='E5 Prototyping Framework',
    version='0.4.dev0',
    url='https://github.com/jcgronde/e5',
    license='NONE',
    author='Jeroen van Grondelle',
    author_email='jeroen@vangrondelle.com',
    description='A framework for doing event analytics',
    long_description=read('README.md'),
    packages=['e5', 'e5.events', 'e5.portal', 'e5.auth', 'e5.data', 'e5.algorithms'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8',
        'python-dateutil',
        'pymongo',
        'pandas==0.19.2',
        'onetimepass',
        'pyqrcode',
        'flask-login==0.4.0',
        'inflection',
        'Werkzeug==0.12.1',
        'flask_jwt'
    ]
)
