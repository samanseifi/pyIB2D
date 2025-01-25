from setuptools import setup, find_packages

setup(
    name='pyIB2D',
    version='0.1.0',
    description='A 2D immersed boundary simulation python code',
    author='Saman Seifi',
    author_email='saman.seyfi@gmail.com',
    licence='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy',
        'h5py',
        'imagio',
    ],
)
