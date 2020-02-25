from setuptools import setup, find_packages

setup(
    name='dslinter',
    version='0.0.1',
    description='A useful module',
    author='Man Foo',
    author_email='foomail@foo.com',
    packages=find_packages(),
    install_requires=['pylint>=2.0', 'astroid'],
)
