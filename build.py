import os

from conan.packager import ConanMultiPackager
from conans import tools

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name=False, pure_c=False)
    builder.run()
    with tools.chdir(os.path.join("sub", "gssapi")):
        builder = ConanMultiPackager()
        builder.add_common_builds(shared_option_name=False, pure_c=False)
        builder.run()
    with tools.chdir(os.path.join("sub", "winextra")):
        builder = ConanMultiPackager()
        builder.add_common_builds(shared_option_name=False, pure_c=False)
        builder.run()
