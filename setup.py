"""
Documentation
"""

from distutils.core import setup
from src.dockurl import __version__

mod_name = 'dockurl'
setup(name=mod_name,
      version=__version__,
      package_dir={'': 'src'},
      packages=['dockurl'],
      package_data={mod_name: ['../../README.md', '../../dockurl.yml.template']},
      url='https://hub.docker.com/r/wilddeej/',
      author='deej Howard',
      author_email='wilddeej@gmail.com',
      requires=['pyshorteners'],
     )

