from robot_engine.utility import cat_version

host = '127.0.0.1'
path = '34.220.114.159:/usr/local/webapps/bestwestern-adapter/WEB-INF/classes/git.properties'

print (cat_version(host, path))
