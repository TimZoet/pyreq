from abc import abstractmethod
import os
import re

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import load

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

    settings = "os", "compiler", "build_type", "arch"
    
    options = {
        "fPIC": [True, False],
        "build_examples": [True, False],
        "build_manual": [True, False],
        "build_tests": [True, False],
        "manual_repository": ["ANY"]
    }
    
    default_options = {
        "fPIC": True,
        "build_examples": False,
        "build_manual": False,
        "build_tests": False,
        "manual_repository": ""
    }

    ############################################################################
    ## Base methods.                                                          ##
    ############################################################################
    
    @classmethod
    def set_version(cls, conan_file, filename, varname):
        content = load(conan_file, os.path.join(conan_file.recipe_folder, filename))
        version = re.search("set\({} (\d+\.\d+\.\d+)\)".format(varname), content).group(1)
        conan_file.version = version.strip()
    
    @classmethod
    def config_options(cls, conan_file):
        pass
    
    # Getting weird errors when the method is called configure.
    # Not sure why all the others don't have the same problem...
    @classmethod
    def configure2(cls, conan_file):
        if not conan_file.options.build_manual:
            del conan_file.options.manual_repository

    @classmethod
    def requirements(cls, conan_file):
        conan_file.requires("cmake-modules/1.0.0@timzoet/github_actions")
    
    @classmethod
    def generate_toolchain(cls, conan_file):
        tc = CMakeToolchain(conan_file)
        tc.user_presets_path = None
        tc.variables["USE_CONAN"] = True
        tc.variables["CMAKE_TEMPLATE_DIR"] = os.path.dirname(conan_file.dependencies["cmake-modules"].cpp_info.components[None].includedir).replace(os.sep, "/")
        if conan_file.options.build_examples:
            tc.variables["BUILD_EXAMPLES"] = True
        if conan_file.options.build_manual:
            tc.variables["BUILD_MANUAL"] = True
            tc.variables["MANUAL_REPOSITORY"] = conan_file.options.manual_repository
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
        return cmake

class PyReq(ConanFile):
    name = "pyreq"
    version = "1.0.0"
    description = "Conan package to be reused through python_requires."
    url = "https://github.com/TimZoet/pyreq"
    license = "GNU AFFERO GENERAL PUBLIC LICENSE Version 3"
    author = "Tim Zoet"
    package_type = "python-require"
