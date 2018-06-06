import os

from conan.packager import ConanMultiPackager
from conans import tools

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name=False, pure_c=False)
    builder.run()
    # CONAN_REFERENCE: "krb5/1.16.1"
    name, ver = os.environ["CONAN_REFERENCE"].split("/", 1)
    with tools.chdir(os.path.join("sub", "gssapi")):
        os.environ["CONAN_REFERENCE"] = "krb5-gssapi/" + ver
        builder = ConanMultiPackager()
        builder.add_common_builds(shared_option_name=False, pure_c=False)
        builder.run()
    with tools.chdir(os.path.join("sub", "winextra")):
        os.environ["CONAN_REFERENCE"] = "krb5-winextra/" + ver
        builder = ConanMultiPackager()
        builder.add_common_builds(shared_option_name=False, pure_c=False)
        builder.run()
