import os

from conans import ConanFile

class Kerberos5GssAPI(ConanFile):
    name = "krb5-gssapi"
    version = "1.16.1"
    build_requires = "krb5/1.16.1@rion/stable"
    keep_imports = True
    license = "MIT"
    url = "https://github.com/krb5/krb5.git"
    description = "MIT Kerberos V: gssapi libs"
    settings = "os", "compiler", "build_type", "arch"

    def imports(self):
        self.copy("*.h", dst="include", src="include")
        for n in ["comerr","gssapi","k5sprt","krb5_","wshelp"]:
            self.copy(n + "*.dll",   dst="bin", src="bin")
            self.copy(n + "*.so",    dst="bin", src="bin")
            self.copy(n + "*.dylib", dst="bin", src="bin")
            self.copy(n + "*.a",     dst="lib", src="lib")
            self.copy(n + "*.lib",   dst="lib", src="lib")
        
        
    def package(self):
        self.copy("bin/*")
        self.copy("lib/*")
        self.copy("include/*")