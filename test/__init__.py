# import requests
#
# r = requests.get("http://%s/test/log/%s" % ('35.166.141.57:51234', '999'), timeout=5)
#
# print (r.content)


from datetime import datetime
import time


date1 = datetime.now()
time.sleep(2)
print ((datetime.now()-date1).minute)