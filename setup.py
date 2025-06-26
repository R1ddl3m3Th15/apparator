from setuptools import setup, find_packages

setup(
    name='apparator',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'playwright',
        'python-dotenv',
    ],
    extras_require={
        'dev': ['pytest'],
    },
    description='Prototype for programmatically collecting coding challenge submissions using Playwright.',
    author='Unknown',
)
