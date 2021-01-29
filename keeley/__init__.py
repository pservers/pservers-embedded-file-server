#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os


"""
access method:
    http-ui r
    http-ui rw       (user: rw)
    http-webdav r    (url-postfix: /webdav)
    http-webdav rw   (url-postfix: /webdav) (user: rw)
    httpdir r        (url-postfix: /pub)

we don't support ftp-protocol because very few server/client supports one-server-multiple-domain.
"""


def start(params):
    selfDir = os.path.dirname(os.path.realpath(__file__))
    domainName = params["domain-name"]
    dataDir = params["data-directory"]
    tmpDir = params["temp-directory"]
    webRootDir = params["webroot-directory"]

    # webdav directory in root directory
    webdavDir = os.path.join(webRootDir, "webdav")
    os.symlink(dataDir, webdavDir)

    # pub directory in root directory
    pubDir = os.path.join(webRootDir, "pub")
    os.symlink(dataDir, pubDir)

    # static files in root directory
    os.symlink(os.path.join(selfDir, "index.html"), os.path.join(webRootDir, "index.html"))

    buf = ''
    buf += 'ServerName %s\n' % (domainName)
    buf += 'DocumentRoot "%s"\n' % (webRootDir)
    buf += 'DavLockDB "%s"\n' % (os.path.join(tmpDir, "DavLock"))
    buf += '<Directory "%s">\n' % (webRootDir)
    buf += '    Require all granted\n'
    buf += '</Directory>\n'
    buf += '<Directory "%s">\n' % (webdavDir)
    buf += '    Dav filesystem\n'
    buf += '    Require all granted\n'
    buf += '</Directory>\n'
    buf += '<Directory "%s">\n' % (pubDir)
    buf += '    Options Indexes\n'
    buf += '    Require all granted\n'
    buf += '</Directory>\n'

    # return result
    cfg = {
        "module-dependencies": [
            "mod_dav.so",
            "mod_dav_fs.so",
            "mod_dav_lock.so",
        ],
        "config-segment": buf,
    }
    privateData = None
    return (cfg, privateData)


def stop(private_data):
    pass
