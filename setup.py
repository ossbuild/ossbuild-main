from setuptools import setup, find_packages

setup(
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
