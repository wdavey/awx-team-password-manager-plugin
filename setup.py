#!/usr/bin/env python3

from setuptools import setup

requirements = [
    'certifi',
    'urllib3'
]

setup(
    name='awx-team-password-manager-plugin',
    version='1.0.0',
    author='William Davey @ Pawsey Supercomputing Centre',
    author_email='wdavey@pawsey.org.au',
    description='Credentials plugin to TPM for AWX',
    long_description='Credentials plugin for AWX, allowing access to credentials stored in Team Password Manager',
    license='Apache License 2.0',
    keywords=['ansible', 'awx', 'team password manager'],
    url='https://github.com/wdavey/awx-team-password-manager-plugin',
    packages=['awx_team_password_manager_plugin'],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[],
    install_requires=requirements,
    entry_points = {
        'awx.credential_plugins': [
            'tpm_plugin = awx_team_password_manager_plugin:tpm_plugin',
        ]
    }
)
