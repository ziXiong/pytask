# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    version='1.0',
    name='pytask',
    description='A Database based Python task runner',
    author='quezixiong',
    author_email='quezixiong@qq.com',
    url='http://github.com/z1xiong/pytask',
    packages=('pytask',),
    package_dir={'pytask': 'pytask'},
    install_requires=(
        'SQLAlchemy',
    )
)
