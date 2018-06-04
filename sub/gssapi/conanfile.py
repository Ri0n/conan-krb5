from conans import ConanFile

class Kerberos5WinExtra(ConanFile):
    name = "krb5-winextra"
    version = "1.16.1"
    build_requires = "krb5-gssapi/1.16.1@rion/testing"
    keep_imports = True

    def imports(self):
        for n in ["kfwlogon","krbcc","leashw","xpprof"]:
			self.copy(n + "*.dll",   dst="bin")
			self.copy(n + "*.so",    dst="bin")
			self.copy(n + "*.dylib", dst="bin")
			self.copy(n + "*.a",     dst="lib")
			self.copy(n + "*.lib",   dst="lib")
		
		
    def package(self):
        self.copy("*")