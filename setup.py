from setuptools import setup, find_packages


setup(
    name='cirrus-run',
    version='0.1.0',
    description='Command line tool to execute jobs in Cirrus CI',
    url='https://github.com/sio/cirrus-run',
    author='Vitaly Potyarkin',
    author_email='sio.wtf@gmail.com',
    license='Apache-2.0',
    platforms='any',
    entry_points={
        'console_scripts': [
            'cirrus-run=cirrus_run.cli:main',
        ],
    },
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    extras_require={ },
    python_requires='>=3.4',
    zip_safe=True,
)
