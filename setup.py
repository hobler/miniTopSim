from setuptools import setup, find_packages

setup(
    name='minitopsim',
    packages=find_packages(where='.'),
    package_dir={'': '.'},
    package_data={'minitopsim': ['parameters.db', 'tables/*']},
    install_requires=['numpy', 'scipy', 'matplotlib']
)
