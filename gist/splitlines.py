__author__ = 'Zhenyu'

import json


t = 'Traceback (most recent call last):\n  File "/Users/Zhenyu/Working/projects/appdriver/suite/runner.py", line 76, in <module>\n    case(config)\n  File "/Users/Zhenyu/Working/projects/appdriver/suite/receipt/suite_receipt.py", line 125, in case4_receipts_list_view\n    driver.send_keys("email address", email, PARTIAL_TEXT)\nNameError: global name \'email\' is not defined\n'

tt = t.splitlines()
print json.dumps(tt, indent=4)