"""Minimal setup.py for C++ extensions using pybind11.

All package metadata is defined in pyproject.toml.
This file only defines the C++ extensions since pybind11 requires
special handling that's easier to do in Python code.

With PEP 517/518, setuptools will read metadata from pyproject.toml
and merge it with the ext_modules defined here.
"""

from pathlib import Path
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

# Get project root (setup.py directory)
project_root = Path(__file__).parent

# Use relative paths from setup.py directory (required by setuptools)
# Paths must be relative, not absolute
ext_modules = [
    Pybind11Extension(
        "rna_map_mini._bit_vector_cpp",
        [
            "cpp/src/bit_vector_generator.cpp",
            "cpp/src/bindings.cpp",
        ],
        include_dirs=["cpp/include"],
        cxx_std=17,
        language="c++",
    ),
]

# Minimal setup() call - metadata comes from pyproject.toml
# This is only needed to register the C++ extensions
setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)

