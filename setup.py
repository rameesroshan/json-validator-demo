import setuptools

NAME = 'jsonvalidator'

setuptools.setup(
    name=NAME,
    version='0.0.1',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'run-validator = jsonvalidator.__main__:main'
        ],
    },
)