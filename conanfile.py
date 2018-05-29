import os
import sys

from contextlib import contextmanager

from conans import ConanFile, tools
from conans.client.tools.files import which, _path_equals
from conans.errors import ConanException
from conans.tools import environment_append

@contextmanager
def remove_from_path_wrong_version(command, is_valid_checker):
    curpath = os.getenv("PATH")
    first_it = True
    for n in range(30):
        if not first_it:
            with environment_append({"PATH": curpath}):
                the_command = which(command)
        else:
            the_command = which(command)
            first_it = False

        if not the_command or is_valid_checker(the_command):
            break
        new_path = []
        for entry in curpath.split(os.pathsep):
            if not _path_equals(entry, os.path.dirname(the_command)):
                new_path.append(entry)

        curpath = os.pathsep.join(new_path)
    else:

        raise ConanException("Error in tools.remove_from_path!! couldn't remove the tool '%s' "
                             "from the path after 30 attempts, still found in '%s' this is a Conan client bug, please open an issue at: "
                             "https://github.com/conan-io/conan\n\nPATH=%s" % (command, the_command, os.getenv("PATH")))

    with environment_append({"PATH": curpath}):
        yield

class Krb5Conan(ConanFile):
    name = "krb5"
    version = "1.16.1"
    license = "MIT"
    url = "https://github.com/krb5/krb5.git"
    description = "MIT Kerberos V"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True]}
    default_options = "shared=True"
    
    krb5_commit = "9ef59b469dc433cc52860db6196e5e47c5ec7817" # 1.16.1 + windows fixes

    def build_requirements(self):
        # useful for example for conditional build_requires
        if self.settings.compiler == "Visual Studio":
            self.build_requires("strawberryperl/5.26.0@conan/stable")
            self.build_requires("msys2_installer/latest@bincrafters/stable") # for cat and sed
    
    def source(self):
        self.run("git clone https://github.com/krb5/krb5.git " + self.subfolder)
        self.run("cd %s && git checkout %s" % (self.subfolder, self.krb5_commit))

    @property
    def subfolder(self):
        return self.name + "-" + self.version
        
    # copied from OpenSSL recipe
    def run_in_src(self, command, show_output=False, cwd="."):
        if not show_output and self.settings.os != "Windows":
            command += ' | while read line; do printf "%c" .; done'
            # pipe doesn't fail if first part fails
            command = 'bash -l -c -o pipefail "%s"' % command.replace('"', '\\"')
        with tools.chdir(self.subfolder):
            self.run(command, cwd=cwd)
        self.output.writeln(" ")
    
    # copied from OpenSSL recipe    
    def visual_build(self):
        self.run_in_src("perl --version")

        self.output.warn("----------MAKE Kerberos FOR WINDOWS. %s-------------" % self.version)
        debug = "" if self.settings.build_type == "Debug" else "NODEBUG=1"
        arch = "i386" if self.settings.arch == "x86" else "AMD64"
        
        config_options_string = "NO_LEASH=1 " + debug
        #configure_type = debug + "VC-WIN" + arch
        #no_asm = "no-asm" if self.options.no_asm else ""
        # Will output binaries to ./binaries
        with tools.vcvars(self.settings, filter_known_paths=False):
            prep_command = "nmake -f Makefile.in prep-windows"
            self.output.warn(prep_command)
            self.run_in_src(prep_command, show_output=True, cwd="src")
            
            os.environ['CPU'] = arch
            os.environ['KRB_INSTALL_DIR'] = os.path.join(os.getcwd(), "conan_install", str(self.settings.arch))
            whole_command = "nmake %s" % config_options_string
            self.output.warn(whole_command + " clean")
            self.run_in_src(whole_command + " clean", cwd="src")
            
            with remove_from_path_wrong_version("link", lambda p: "Microsoft Visual Studio" in p):
                self.output.warn(whole_command)
                self.run_in_src(whole_command, show_output=True, cwd="src")
        
    def build(self):
        if self.settings.compiler == "Visual Studio":
            self.visual_build()
        else:
            raise Exception("Unsupported operating system: %s" % self.settings.os)

    def package(self):
        self.copy("lmdb.h", dst="include", src="lmdb\\libraries\\liblmdb")
        self.copy("*lmdb*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        prefix = ["lib",""][self.options.shared == True]
        postfix = ["","d"][self.settings.get_safe("build_type") == "Debug"]
        self.cpp_info.libs = [prefix + "lmdb" + postfix]

