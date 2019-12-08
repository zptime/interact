#!/usr/bin/env bash
. /opt/virt/interact/bin/activate
cd ..
gunicorn --config gunicorn.conf interact.wsgi:application --daemon
/etc/init.d/celeryd_interact start
/etc/init.d/celerybeat_interact start
