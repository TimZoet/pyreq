from abc import abstractmethod
import os
import re

from conans import ConanFile, CMake
from conans.tools import load
from conan.tools.cmake import CMakeToolchain, CMakeDeps

class BaseConan:
    ############################################################################
    ## Package info.                                                          ##
    ############################################################################

    homepage = "https://github.com/TimZoet"
    
    license = "GNU AFFERO GENERAL PUBLIC LICENSE Version 3"
    
    author = "Tim Zoet"
    
    @property
    def default_user(self):
        return "timzoet"
    
    @property
    def default_channel(self):
        return "stable"

    ############################################################################
    ## Settings.                                                              ##
    ############################################################################

    generators = "CMakeDeps", "CMakeToolchain"
    
    settings = "os", "compiler", "build_type", "arch"
    
    options = {
        "fPIC": [True, False],
        "build_examples": [True, False],
        "build_tests": [True, False]
    }
    
    default_options = {
        "fPIC": True,
        "build_examples": False,
        "build_tests": False
    }

    ############################################################################
    ## Base methods.                                                          ##
    ############################################################################
    
    @classmethod
    def set_version(cls, conan_file, filename, varname):
        content = load(os.path.join(conan_file.recipe_folder, filename))
        version = re.search("set\({} (\d+\.\d+\.\d+)\)".format(varname), content).group(1)
        conan_file.version = version.strip()

    @classmethod
    def requirements(cls, conan_file):
        pass
    
    @classmethod
    def generate_toolchain(cls, conan_file):
        tc = CMakeToolchain(conan_file)
        tc.variables["USE_CONAN"] = True
        if conan_file.options.build_examples:
            tc.variables["BUILD_EXAMPLES"] = True
        if conan_file.options.build_tests:
            tc.variables["BUILD_TESTS"] = True
        return tc
    
    @classmethod
    def generate_deps(cls, conan_file):
        deps = CMakeDeps(conan_file)
        return deps
    
    @classmethod
    def configure_cmake(cls, conan_file):
        cmake = CMake(conan_file)
        cmake.definitions["USE_CONAN"] = True
        if conan_file.options.build_examples:
            cmake.definitions["BUILD_EXAMPLES"] = True
        if conan_file.options.build_tests:
            cmake.definitions["BUILD_TESTS"] = True
        return cmake

class PyReq(ConanFile):
    name = "pyreq"
    version = "1.0.0"
    description = "Conan package to be reused through python_requires."
    url = "https://github.com/TimZoet/pyreq"
    license = "GNU AFFERO GENERAL PUBLIC LICENSE Version 3"
    author = "Tim Zoet"
