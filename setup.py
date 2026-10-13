"""Configuração da extensão C++ opcional/embutida do Lopus-AI."""

from __future__ import annotations

import sys

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

compile_args = ["/utf-8"] if sys.platform == "win32" else ["-Wall", "-Wextra", "-Wpedantic"]
define_macros = [("NOMINMAX", "1")] if sys.platform == "win32" else []
libraries = ["user32", "gdi32"] if sys.platform == "win32" else []

ext_modules = [
    Pybind11Extension(
        "lopus_native",
        [
            "native/src/module.cpp",
            "native/src/system.cpp",
            "native/src/input.cpp",
            "native/src/screen.cpp",
        ],
        include_dirs=["native/include"],
        define_macros=define_macros,
        libraries=libraries,
        extra_compile_args=compile_args,
        cxx_std=20,
        optional=True,
    )
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
