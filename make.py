import os
import hashlib
import subprocess
import shutil
import sys

__version__ = (0, 0, 0)
pkgname = ""
pkgdesc = ''
owner = 'Franklyn Tackitt <franklyn@tackitt.net>'
owner_github = 'kageurufu'

# Through black magic, update those variables
execfile('./app/version.py', globals(), locals())

_PKGBUILD = """# Maintainer: %(owner)s
pkgname=%(pkgname)s
pkgver=%(version)s
pkgrel=1
pkgdesc="%(pkgdesc)s"
arch=(any)
url="https://github.com/%(owner_github)s/$pkgname"
license=('GPL')
depends=('docker'
         'systemd-docker')
makedepends=('python2')
backup=("etc/conf.d/$pkgname")
source=("$pkgname-$pkgver.tar.gz"
        "$pkgname.service"
        "$pkgname.conf")
md5sums=('%(md5sum)s'
         '%(service_md5sum)s'
         '%(conf_md5sum)s')

package() {
    mkdir -p $pkgdir/usr/share/webapps/$pkgname/
    cp -r $srcdir/$pkgname-$pkgver/.config \\
                $srcdir/$pkgname-$pkgver/.dockerignore \\
                $srcdir/$pkgname-$pkgver/* \\
                 $pkgdir/usr/share/webapps/$pkgname
    install -Dm644 $pkgname.service $pkgdir/usr/lib/systemd/system/$pkgname.service
    install -Dm644 $pkgname.conf $pkgdir/etc/conf.d/$pkgname
}"""

_CONF = '''# Leave this, unless you want live debugging which is a terrible idea
ENVIRONMENT="PRODUCTION"

# Port to expose %(pkgname)s on, defaults to 80
PORT="80"'''

_SERVICE = '''[Unit]
Description=%(pkgname)s
After=docker.service
Requires=docker.service

[Service]
EnvironmentFile=/etc/conf.d/%(pkgname)s
ExecStartPre=/usr/bin/docker build -t %%n /usr/share/webapps/%(pkgname)s
ExecStart=/usr/bin/systemd-docker --env run --rm --name %%n -p ${PORT}:80 %%n
Restart=always
RestartSec=10s
Type=notify
NotifyAccess=all
TimeoutStartSec=240
TimeoutStopSec=15

[Install]
WantedBy=multi-user.target
'''


def write_package_file(f, d):
    with open(os.path.join('package', f), 'w') as o:
        o.write(d)


def make():
    if not os.path.isdir("package"):
        os.mkdir("package")

    # Make the source distribution
    subprocess.call(['/usr/bin/env python2 setup.py sdist'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # Md5sum it, and write to package at the same time
    with open("dist/" + pkgname + "-%d.%d.%d.tar.gz" % __version__, "rb") as i:
        data = i.read()
        md5sum = hashlib.md5(data).hexdigest()
        with open("package/" + pkgname + "-%d.%d.%d.tar.gz" % __version__, 'wb') as o:
            o.write(data)

    CONF = _CONF % dict(pkgname=pkgname, pkgdesc=pkgdesc, owner=owner, owner_github=owner_github)
    SERVICE = _SERVICE % dict(pkgname=pkgname, pkgdesc=pkgdesc, owner=owner, owner_github=owner_github)

    PKGBUILD = _PKGBUILD % dict(pkgname=pkgname,
                                pkgdesc=pkgdesc,
                                owner=owner,
                                owner_github=owner_github,
                                version="%d.%d.%d" % __version__,
                                md5sum=md5sum,
                                service_md5sum=hashlib.md5(SERVICE).hexdigest(),
                                conf_md5sum=hashlib.md5(CONF).hexdigest())

    write_package_file(pkgname + '.service', SERVICE)
    write_package_file(pkgname + '.conf', CONF)
    write_package_file('PKGBUILD', PKGBUILD)

    subprocess.call(['/usr/bin/makepkg -cCf'], cwd=os.path.join('.', 'package'), shell=True)


def clean():
    for i in ('build', 'dist', 'package', pkgname.replace("-", "_") + '.egg-info'):
        print("rm -r " + i)
        shutil.rmtree(i, ignore_errors=True)


def install():
    subprocess.call(['/usr/bin/sudo pacman -U package/' + pkgname + "-%d.%d.%d-1-any.pkg.tar.xz" % __version__],
                    shell=True)


if __name__ == '__main__':
    if 'Arch Linux' not in open('/etc/os-release', 'r').read():
        print("make only available on Arch Linux")
        sys.exit(1)

    if sys.argv[1] == 'clean':
        clean()
    elif sys.argv[1] == 'make':
        make()
    elif sys.argv[1] == 'install':
        install()
    else:
        clean()
        make()
