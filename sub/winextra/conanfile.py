import os

from conans import ConanFile

class Kerberos5WinExtra(ConanFile):
    name = "krb5-winextra"
    version = "1.16.1"
    requires = "krb5-gssapi/1.16.1@rion/stable"
    build_requires = "krb5/1.16.1@rion/stable"
    keep_imports = True
    license = "MIT"
    url = "https://github.com/krb5/krb5.git"
    description = "MIT Kerberos V: Windows extra libs"
    settings = "os", "compiler", "build_type", "arch"

    def imports(self):
        for n in ["kfwlogon","krbcc","leashw","xpprof"]:
            self.copy(n + "*.dll",   dst="bin", src="bin")
            self.copy(n + "*.so",    dst="bin", src="bin")
            self.copy(n + "*.dylib", dst="bin", src="bin")
            self.copy(n + "*.a",     dst="lib", src="lib")
            self.copy(n + "*.lib",   dst="lib", src="lib")

    def package(self):
        self.copy("bin/*")
        self.copy("lib/*")