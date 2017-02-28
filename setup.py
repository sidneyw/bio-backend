from setuptools import setup, find_packages


setup(
    name='bio',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
