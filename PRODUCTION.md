I'm using nginx, uwsgi, and upstart.

The nginx config file goes here `/etc/nginx/sites-available/presentr.conf`

The uwsgi config file goes here `/etc/uwsgi.ini`

The upstart config file goes here `/etc/init/uwsgi.conf`

You need to run this from time to time: `sudo service uwsgi restart`
