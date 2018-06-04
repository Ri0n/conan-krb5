from conans import ConanFile

class Kerberos5GssAPI(ConanFile):
    name = "krb5-gssapi"
    version = "1.16.1"
    build_requires = "krb5/1.16.1@rion/testing"
    keep_imports = True

    def imports(self):
        self.copy("*.h", dst="include", src=os.path.join(install_dir, "include"))
		for n in ["comerr","gssapi","k5sprt","krb5_","wshelp"]:
			self.copy(n + "*.dll",   dst="bin")
			self.copy(n + "*.so",    dst="bin")
			self.copy(n + "*.dylib", dst="bin")
			self.copy(n + "*.a",     dst="lib")
			self.copy(n + "*.lib",   dst="lib")
		
		
    def package(self):
        self.copy("*")