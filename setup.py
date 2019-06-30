import os,sys
from setuptools import setup

# For regular package imports, not 'import .packagename'
modpath = os.path.abspath(os.path.split(sys.argv[0])[0]) + '/astron'
sys.path.append(modpath)
import astron

setup(name=astron.__name__,
      version=astron.__version__,
      description='...',
      url='...',
      author='...',
      author_email='',
      license='MIT',
      install_requires=['autopep8'],
      packages=['gravityassist'], 
      include_package_data=True,
      zip_safe=True)
