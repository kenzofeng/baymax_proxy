#!/usr/bin/env bash
#cd baymaxfront
#npm run build
#cd  ..
rm -rf baymaxproxy.tar.gz
tar -zcvf  baymaxproxy.tar.gz ./Baymax_Proxy/*.py ./baymaxfront/dist/ ./proxy/*.py ./proxy/handler/*.py  ./proxy/urls/*.py ./robot_engine/*.py ./Pipfile ./Pipfile.lock ./manage.py ./templates/
#scp baymaxproxy.tar.gz upload@10.200.106.41:~
scp -i /home/feng/abc.txt baymaxproxy.tar.gz derbyqa@52.89.237.133:~