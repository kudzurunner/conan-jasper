from conans import ConanFile, CMake, tools
import os

class JasperConan(ConanFile):
    name = "jasper"
    version = "2.0.14"
    license = "https://raw.githubusercontent.com/mdadams/jasper/master/LICENSE"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-jasper"
    description = "JasPer Image Processing/Coding Tool Kit"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "enable_doc": [True, False],
        "enable_programs": [True, False]
    }
    default_options = {
        "shared": True,
        "enable_doc": False,
        "enable_programs": False
    }
    requires = "libjpeg-turbo/2.0.1@kudzurunner/stable"
    source_name = "{}-version-{}".format(name, version)
    generators = "cmake"

    def configure(self):
        del self.settings.compiler.libcxx
        self.options["libjpeg-turbo"].shared = self.options.shared

    def source(self):
        archive_name = "version-{}.tar.gz".format(self.version)
        url = "https://github.com/mdadams/jasper/archive/{}".format(archive_name)

        tools.download(url, filename=archive_name)
        tools.untargz(filename=archive_name)
        os.remove(archive_name)

        tools.replace_in_file(
            "{}/CMakeLists.txt".format(self.source_name), "project(JasPer LANGUAGES C)",
            '''project(JasPer LANGUAGES C)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()'''
        )

        # fix version
        tools.replace_in_file(
            "{}/src/libjasper/include/jasper/jas_config.h.in".format(self.source_name), "#define JAS_VERSION \"unknown\"",
            "#define JAS_VERSION \"@JAS_VERSION@\""
        )

    def build(self):
        cmake = CMake(self)
        cmake.definitions['JAS_ENABLE_SHARED'] = self.options.shared;
        cmake.definitions['JAS_ENABLE_LIBJPEG'] = True
        cmake.definitions['JAS_ENABLE_OPENGL'] = False
        cmake.definitions['JAS_ENABLE_STRICT'] = False
        cmake.definitions['JAS_ENABLE_AUTOMATIC_DEPENDENCIES'] = False
        cmake.definitions['JAS_LOCAL'] = False
        cmake.definitions['JAS_ENABLE_DOC'] = self.options.enable_doc
        cmake.definitions['JAS_ENABLE_PROGRAMS'] = self.options.enable_programs
        cmake.configure(source_folder=self.source_name)
        cmake.build()

    def package(self):
        self.copy("LICENSE", src=self.source_name)

        self.copy("*.h", dst="include", src="{}/src/libjasper/include".format(self.source_name))
        self.copy("*.h", dst="include", src="src/libjasper/include")

        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["jasper"]