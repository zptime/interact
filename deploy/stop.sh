#!/usr/bin/env bash
for i in `ps -ef|grep interact.wsgi|grep -v grep|awk '{print $2}'`
do
kill -9 $i
done
/etc/init.d/celeryd_interact stop
/etc/init.d/celerybeat_interact stop
