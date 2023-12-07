#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers, using the
function do_deploy
"""
from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = '/path/to/your/private/key.pem'


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
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(archive_no_ext,
                                                  archive_no_ext))

        # Remove the web_static folder
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            archive_no_ext))

        # Remove the old symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(
            archive_no_ext))

        print('New version deployed!')
        return True
    except Exception as e:
        print(e)
        return False
