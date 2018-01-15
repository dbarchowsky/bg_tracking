from setuptools import setup


setup(
    name='bg_tracking',
    packages=['bg_tracking'],
    include_package_data=True,
    install_requires=[
        'flask',
        'peewee',
        'markupsafe',
    ],
)
