"""Setup."""
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='tap-shopify-partners',
    version='0.1.0',
    description='Singer.io tap for extracting data from Shopify Partners',
    author='Yoast',
    url='https://github.com/Yoast/singer-tap-shopify-partners',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['tap_shopify_partners'],
    install_requires=[
        'httpx[http2]~=0.16.1',
        'python-dateutil~=2.8.1',
        'singer-python~=5.10.0',
    ],
    entry_points="""
        [console_scripts]
        tap-shopify-partners=tap_shopify_partners:main
    """,
    packages=['tap-shopify-partners'],
    package_data={
        'schemas': ['tap-shopify-partners/schemas/*.json'],
    },
    include_package_data=True,
)
