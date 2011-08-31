from distutils.core import setup

from constants import __version__

name = 'constants'

setup(
    name=name,
    version=__version__,
    author='Steven Armstrong',
    author_email='steven-%s@armstrong.cc' % name,
    url='http://github.com/asteven/%s/' % name,
    description='Constants implementation',
    py_modules=[name],
)

