VERSION='0.4.0'


from setuptools import setup, find_packages


with open("README.md") as readme:
    long_description = readme.read()


setup(
    name='cirrus-run',
    version=VERSION,
    description='Command line tool to execute jobs in Cirrus CI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sio/cirrus-run',
    download_url='https://github.com/sio/cirrus-run/archive/v{}.tar.gz'.format(VERSION),
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
        'Jinja2',
        'requests',
    ],
    extras_require={ },
    python_requires='>=3.4',
    zip_safe=True,
    keywords=[
        'api',
        'ci',
        'cirrus-ci',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development',
    ],
)
