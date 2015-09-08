from setuptools import setup

__version__ = (0, 0, 0)
pkgname = ''
pkgdesc = ''
# Through black magic, get the real version ;)
execfile('./app/version.py', globals(), locals())


def parse_requirements():
    reqs = []
    with open("requirements.txt") as f:
        for req in f:
            req = req.strip()
            if req.startswith("#"):
                continue
            reqs.append(req)
    return reqs


setup(
    name=pkgname,
    author='Disruptive Labs',
    author_email='team+' + pkgname + '@comanage.com',
    url='http://github.com/DisruptiveLabs/' + pkgname,
    version='%d.%d.%d' % __version__,
    description=pkgdesc,
    long_description=open('README.rst').read(),
    package_dir={pkgname: 'app'},
    entry_points={
        'console_scripts': [pkgname + '=manage:manager.run']
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_requirements(),
)
