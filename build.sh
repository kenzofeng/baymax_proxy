cd baymaxfront
npm run build
cd  ..
rm -rf baymaxproxy.tar.gz
tar -zcvf  baymaxproxy.tar.gz ./Baymax_Proxy/*.py ./baymaxfront/dist/ ./robot_engine/*.py