import setuptools
import os

REQUIRED = [
    'flask==1.0.2', 'python-dateutil', 'flask-cors', 'hiredis'
]

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.rst') as f:
    license = f.read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


resources = package_files('resources/')

setuptools.setup(
    name='juan_libs',
    version='0.1.0',
    description='Reusable libraries for a recruiting process',
    long_description=readme,
    author='Juan Pablo Salamanca Ramirez',
    author_email='jpsalamarcara@unal.edu.co',
    url='https://github.com/jpsalamarcara/juan_salamanca_test',
    license=license,
    packages=setuptools.find_packages(exclude=('test', 'docs', 'dev')),
    install_requires=REQUIRED,
    package_data={'': resources},
    include_package_data=True
)