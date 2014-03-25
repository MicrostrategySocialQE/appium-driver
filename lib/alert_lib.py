'''
Wrapper around appium_driver and give combined actions.
'''
from lib import uimap

__author__ = 'Zhenyu'

import time
from lib.appium_driver import AppiumDriver, ElementType


class AlertLib(object):

    def __init__(self, driver, platform="ios"):
        self.driver = driver
        self.platform = platform
        pass

    def click(self, element, element_type=0):
        if isinstance(element, dict):
            element = element[self.platform]
        self.driver.click(element, element_type)

    def send_keys(self, element, keys, element_type=0):
        if isinstance(element, dict):
            element = element[self.platform]
        self.driver.send_keys(element, keys, element_type)

    def try_to_click(self, element, element_type=0):
        if isinstance(element, dict):
            element = element[self.platform]
        self.driver.try_to_click(element, element_type)

    def login(self, account):
        if account['type'] == 'brand':
            self.click(uimap.login.sign_in)
            self.send_keys(uimap.signin.email, account['email'], ElementType.partial_text)
            self.try_to_click('Done')
            self.send_keys(uimap.signin.password, account['password'], ElementType.partial_text)
            self.try_to_click("Done")
            self.click(uimap.signin.submit, ElementType.partial_text)
            time.sleep(2)
            self.try_to_click(uimap.general.geofence_close)
            return True

    def open_tab(self, tabname):
        self.click(uimap.general.sider_bar, ElementType.partial_text)
        self.click(tabname)
        return True

    def logout(self, username):
        self.click(uimap.general.sider_bar, ElementType.partial_text)
        self.click(username, ElementType.partial_text)
        self.click(uimap.account.signout)
        self.click(uimap.account.signoutok)


if __name__ == "__main__":
    d = AppiumDriver()
    account = {
            "email": "kkk@mailinator.com",
            "password": "newman123",
            "type": "brand"
        }

    t = AlertLib(d, 'ios')
    t.login(account)
    t.logout("Kim")




