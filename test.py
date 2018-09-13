from robot_engine import  utility
import os
import svn.local
import svn.remote


try:
    test=r'D:\workspace\baymax_proxy\project\test_automation'
    testpath = os.path.join(test, 'Hilton_adapter')
    if os.path.exists(testpath):
        utility.remove_file(testpath)
        utility.remove_file(testpath)
        utility.remove_file(testpath)
    os.mkdir(testpath)
    r = svn.remote.RemoteClient('https://10.200.107.160:8443/svn/warrior-test/automation/provider_hilton_adapter(NEW_JSON)/trunk')
    r.checkout(testpath)
    l = svn.local.LocalClient(testpath)
    revision_number = l.info()['commit#revision']
    print revision_number
except UnicodeDecodeError:
    pass
except Exception as e:
    pass
