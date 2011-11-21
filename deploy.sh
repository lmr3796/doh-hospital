#!/bin/sh
SERVER_PATH='/srv/www/doh'
cp -Lrf deploy/* $SERVER_PATH
find $SERVER_PATH -type d | xargs chown -R www-data:lmr3796 
find $SERVER_PATH -type d | xargs chmod 774
find $SERVER_PATH -name *doh.json | xargs chmod 644
chmod 554 $SERVER_PATH/*.py
chmod 554 $SERVER_PATH/*.sh
chmod 444 $SERVER_PATH/Beautiful.py
cd $SERVER_PATH
./cron_gen_cache.py
