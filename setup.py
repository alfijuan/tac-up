from setuptools import setup, find_packages

setup(
    name='TAPJAUP2020',
    version='0.1',
    packages=find_packages(),
    url='https://localhost:PORT',
    author='JuanAlfieri',
    author_email='alfieri.juan@gmail.com',
    description='',
    install_requires=[i.strip() for i in open("requirements.txt").readlines()]
)
