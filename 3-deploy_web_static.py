#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers,
using the function deploy
"""
from fabric.api import local, env, run
from os.path import exists
from datetime import datetime
from fabric.operations import put

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = '/path/to/your/private/key.pem'


def do_pack():
    """Create a compressed archive from the contents of web_static"""
    try:
        if not exists("versions"):
            local("mkdir -p versions")

        time_format = "%Y%m%d%H%M%S"
        archive_path = "versions/web_static_{}.tgz".format(
            datetime.utcnow().strftime(time_format)
        )

        local("tar -cvzf {} web_static".format(archive_path))

        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split('/')[-1]
        archive_no_ext = archive_filename.split('.')[0]

        # Upload the archive to /tmp/ on the web server
        put(archive_path, '/tmp/')

        # Create the folder for the new version
        run('mkdir -p /data/web_static/releases/{}'.format(archive_no_ext))

        # Uncompress the archive to the folder
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(
            archive_filename, archive_no_ext))

        # Remove the archive from the server
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents to the proper location
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(archive_no_ext,
                                                   archive_no_ext))

        # Remove the web_static folder
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            archive_no_ext))

        # Remove the old symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{} '
            '/data/web_static/current'.format(archive_no_ext))

        print('New version deployed!')
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """Deploy a new version of your web_static"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
