# -*- coding: utf-8 -*-
from setuptools import setup

__author__ = 'viruzzz-kun'
__version__ = '0.1'


if __name__ == '__main__':
    setup(
        name="bouser_maxwell",
        version=__version__,
        description="Bars.MR Integration service for Bouser",
        long_description='',
        author=__author__,
        author_email="viruzzz.soft@gmail.com",
        license='ISC',
        url="http://github.com/hitsl/bouser_ezekiel",
        packages=["bouser_maxwell", ],
        zip_safe=False,
        package_data={},
        install_requires=[
            'bouser',
            'gtxamqp',
        ],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Plugins",
            "Programming Language :: Python",
        ])
