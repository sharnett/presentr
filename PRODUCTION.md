I'm using nginx, uwsgi, and upstart.

The nginx config file goes here /etc/nginx/sites-available/presentr.conf

The uwsgi config file goes here /etc/uwsgi.ini

For the upstart config file /etc/init/uwsgi.conf, update these two lines appropriately:

You need to run this from time to time: sudo service uwsgi restart