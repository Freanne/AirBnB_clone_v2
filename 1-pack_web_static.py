#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from web_static"""
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Create a compressed archive from the contents of web_static"""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")

        time_format = "%Y%m%d%H%M%S"
        archive_path = "versions/web_static_{}.tgz".format(
            datetime.utcnow().strftime(time_format)
        )

        local("tar -cvzf {} web_static".format(archive_path))

        return archive_path
    except Exception:
        return None
