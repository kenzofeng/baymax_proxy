# import requests
#
# r = requests.get("http://%s/test/log/%s" % ('35.166.141.57:51234', '999'), timeout=5)
#
# print (r.content)

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

from datetime import datetime
import time


date1 = datetime.now()
time.sleep(2)
print (strfdelta((datetime.now()-date1),'{hours}h {minutes}m {seconds}s'))