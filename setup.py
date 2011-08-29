import os
import platform
import shutil
import shlex, subprocess

from setuptools import setup, find_packages
from setuptools.command.install import install as _install

# FIXME: This will only works for installations invoking setup.py but not
#        for bdist_rpm or bdit_msi, where we should pass a post-install script


OSSBUILDENV = '''\
# Sets the environment variables for the toolchain
import os

#os.environ['HOST'] = 'i686-w64-mingw32'
#os.environ['TOOLCHAIN_PREFIX'] = '%s'
'''

class install(_install):
    def run(self):
        _install.run(self)
        self._install_data_files()

    def _install_data_files(self):
        ossbuild_dest = os.path.join(os.environ['HOME'], '.ossbuild')
        patches_dest = os.path.join(ossbuild_dest, 'patches')
        modulesets_dest = os.path.join(ossbuild_dest, 'modulesets')

        patches_src = os.path.abspath('patches')
        modulesets_src = os.path.abspath('modulesets')

        try:
            os.mkdir(ossbuild_dest)
            os.mkdir(patches_dest)
            os.mkdir(modulesets_dest)
        except OSError:
            # dir exists
            pass

        patches = os.listdir(patches_src)
        modulesets = os.listdir(modulesets_src)

        # Copy patches and modulesets to the home directory
        for patch in patches:
            shutil.copy2(os.path.join(patches_src, patch),
                         os.path.join(patches_dest, patch))
        for moduleset in modulesets:
            shutil.copy2(os.path.join(modulesets_src, moduleset),
                         os.path.join(modulesets_dest, moduleset))

        # Save 'ossbuildrc' config file with the module set path
        try:
            f=open(os.path.join(ossbuild_dest, 'ossbuildrc'), 'w+')
            f.write("modulesets_dir = '%s'" % modulesets_dest)
            f.close()
        except IOError, e:
            raise Exception("Could not write 'ossbuilrc': %s", e)
        try:
            f=open(os.path.join(ossbuild_dest, 'ossbuildenv'), 'w+')
            if platform.system() == 'Windows':
                f.write(OSSBUILDENV % 'c:\\MinGW\\bin\\')
            else:
                f.write(OSSBUILDENV % '~/ossbuild/mingw/w32/')
            f.close()
        except IOError, e:
            raise Exception("Could not write 'ossbuilrc': %s", e)

        # ossbuild is now installed, update the modules :)
        p = subprocess.Popen(shlex.split('ossbuild update_moduleset'))


setup(
    cmdclass={'install': install},
    name = "OSSBuild",
    version = "0.1",
    packages = find_packages() + find_packages('jhbuild'),
    package_dir = {'jhbuild' : 'jhbuild/jhbuild'},

    package_data = {
        'ossbuild' : ['*.ossbuildrc'],
        'jhbuild' : ['*.jhbuildrc']},

    entry_points = {
        'console_scripts': [
            'ossbuild = ossbuild.main:main',
        ],
    },

    # metadata for upload to PyPI
    author = "OSSBuild team",
    author_email = "ossbuild@ossbuil.org",
    description = "OSSBuild packaging tool",
    license = "LGPL",
    url = "http://ossbuild.org",
)
