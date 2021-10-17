from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("aoc23.pyx", annotate=True)
    )
