"""The setup for Mailroom distribution."""

from setuptools import setup

setup(
    name='Server Part 3',
    description='Implementation of locally hosted server and client.',
    version=0.1,
    author='Jordan Schatzman, Regenal Grant',
    author_email='j.schatzman@outlook.com',
    license='MIT',
    package_dir={'': 'src'},
    py_modules=['echo_server'],
    extras_require={'test': ['pytest', 'pytest-watch', 'pytest-cov', 'tox']},
)
