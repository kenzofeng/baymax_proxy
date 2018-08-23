#!/usr/bin/env bash
sudo pip install supervisor
sudo cp supervisord.conf /etc/
sudo mkdir -p /etc/supervisor/conf.d/
sudo cp baymax.conf /etc/supervisor/conf.d/
sudo mkdir -p /var/run/supervisord
sudo /usr/local/bin/supervisord -c /etc/supervisord.conf
sed -i '$a sudo /usr/local/bin/supervisord -c /etc/supervisord.conf' /etc/rc.d/rc.local
sed -i '$a sudo supervisorctl start' /etc/rc.d/rc.local
sudo ln -s /usr/local/bin/supervisorctl /usr/bin/supervisorctl