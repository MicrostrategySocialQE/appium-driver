"""
Opens appium server in an individual process.
"""
__author__ = 'Zhenyu'

import os
import signal
import time
import subprocess
import biplist
import logging
from utilities.sim_location_auth import ios_sim_location_authorize


logger = logging.getLogger("__main__")
APPIUM_PATH = os.path.expanduser("~/Working/appium/")


def extract_bundleid_and_authorize(app_path):
    info_path = app_path + "/info.plist"
    if os.path.exists(info_path):
        plist = biplist.readPlist(info_path)
        bundle_id = plist['CFBundleIdentifier']
        ios_sim_location_authorize(bundle_id)
        logger.info("Location service authorized.")


class AppiumServer(object):

    def __init__(self, arguments):
        self.arguments = arguments.split()
        self.process = False

    def run(self):
        args = self.arguments
        self.env = os.environ.copy()
        for arg in args:
            if ".app" in arg:
                extract_bundleid_and_authorize(arg)
                break
            if "pkg" in arg:
                self.env['ANDROID_HOME'] = "/Users/Zhenyu/Working/android-sdk-macosx/"
        self.process = subprocess.Popen(["node", APPIUM_PATH] + self.arguments, env=self.env)
        #print self.process.pid
        logger.info("Starting Appium server...")

    def kill(self):
        if self.process:
            os.kill(self.process.pid, signal.SIGKILL)


if __name__ == "__main__":
    appium_server = AppiumServer("--app-pkg com.alert.trela.demo --app-activity com.alert.ui.activity.DispatchActivity \
    --app /Users/Zhenyu/Desktop/temp/Trela-demo-release.apk --app-wait-activity com.alert.ui.activity.LoginActivity -m")
    appium_server.run()
    appium_server.kill()
    time.sleep(3)
    print "check here!!"