from setuptools import setup, find_packages

setup(
    name='devscript',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'talib',
        'matplotlib',
        'scipy',
        'websocket-client',
        'requests'
    ],
    author='TMM Dev',
    description='DevScript Trading Engine',
    python_requires='>=3.8'
)
