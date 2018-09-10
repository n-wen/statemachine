from setuptools import setup
import sys

if sys.version_info[0] != 3:
    raise Exception("this only work on python3.")

requirements = ['transitions==0.6.8']

setup(
    name="statemachine",
    version="0.0.2",
    url='https://github.com/htwenning/statemachine',
    license='BSD',
    author='wenning',
    author_email='ht.wenning@foxmail.com',
    description='a tool to manage states automatically',
    packages=['statemachine'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
)
