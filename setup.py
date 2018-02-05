from setuptools import setup


setup(
    name='bg_tracking',
    version='0.0.1',
    url='https://github.com/dbarchowsky/bg_tracking/',
    author='Damien Barchowsky',
    author_email='dbarchowsky@gmail.com',
    packages=['bg_tracking'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_wtf',
        'peewee',
        'markupsafe',
        'python-dateutil',
        'wtf-peewee',
    ],
    dependency_links=[
        'https://github.com/coleifer/wtf-peewee/tarball/master#egg=package-3.0.0'
    ],
)
