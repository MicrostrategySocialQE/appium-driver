"""
Verify account from mailinator.com
"""

__author__ = 'Zhenyu'

import requests
import re
import json
from logging import getLogger

log = getLogger("__main__")


def verify_account(email):

    email = email.split("@")[0]

    # get email address
    t = requests.get("http://www.mailinator.com/settt?box="+email)
    address = json.loads(t.text)['address']

    # get messages list
    t = requests.get("http://www.mailinator.com/grab?inbox="+email+"&address="+address)
    messagelist = json.loads(t.text)['maildir']

    log.info(messagelist)
    for message in messagelist:
        if message['subject'] == "Account Verification":
            break

    # get message body
    message = requests.get("http://www.mailinator.com/rendermail.jsp?msgid="+message['id'])

    links = re.findall(r"href=[^\s]+", message.text)
    log.info(links)

    for link in links:
        link = link[6:-1]
        link = link.replace("&#61;", "=").replace("&amp;", '&')
        r = requests.get(link)
        log.info("Send request to: " + link)
        log.info("Request status: " + str(r.status_code))


if __name__ == "__main__":
    verify_account("184617842@madf.com")