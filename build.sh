cd baymaxfron
npm run build
cd  ..
rm -rf baymax.tar.gz
tar -zcvf  baymax.tar.gz ./Baymax_Proxy/*.py ./baymaxfront/dist/ ./robot_engine/*.py