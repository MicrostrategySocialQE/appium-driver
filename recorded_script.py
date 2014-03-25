"""recorded script"""
import time
import os
from lib.appium_driver import AppiumDriver
from lib.appium_server import AppiumServer

NAME = 0  # default value
XPATH = 1
PARTIAL_TEXT = 2


def testing(config):
    driver = config["driver"]

if __name__ == "__main__":
    os.system("ps aux | grep -ie bin/appium | awk '{print $2}' | xargs kill -9")
    time.sleep(1)
    desired_caps = {"device": "iphone simulator", "newCommandTimeout": 60000}
    server = AppiumServer("--app /Users/Zhenyu/Desktop/temp/Trela_magento_test.app")
    server.run()
    time.sleep(3)
    driver = AppiumDriver(desired_caps)
    testing({"driver": driver})
    driver.quit()
    server.kill()
