from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='mezzanine-nexmoverify',
      version=version,
      description="Mezzanine Nexmo Verify Plugin",
      long_description=open("README.rst", 'rb').read().decode('utf-8'),
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Mezzanine",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='mezzanine django nexmo verify',
      author='Krzysztof Pieczara',
      author_email='',
      url='https://github.com/kpnn/mezannine-nexmoverify',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            "django >= 1.6, != 1.6.0, < 1.7",
            "requests >= 2.4.2",
            "mezzanine==3.1.10",
            "bootstrap3",
      ],
      )
