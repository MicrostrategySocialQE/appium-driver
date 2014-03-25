'''
Created on Aug 6, 2013

@author: Zhenyu

Wrapper around WebDriver and give more convinient methods.
'''

import os
import time
import json
import logging
from selenium import webdriver
from lib.pagesource_elements_tree import PageSourceElementsTree
from utilities import xmltodict
from utilities import add_cert


log = logging.getLogger("__main__")


class ElementType:
    name = 0
    xpath = 1
    partial_text = 2


class AppiumDriver(object):
    '''
    driver for Alert apps
    
    Two types of methods:
        1. Element locating methods.
        2. Action performing methods. Perform action on a certain element.
    '''
    
    def __init__(self, desired_caps={}, appium_server="127.0.0.1:4723"):
        """
        Provide the desired capabilities in desired_caps if they are not
        provided as Appium server arguments.
        """
        log.info("Appium driver initiated.")
        self.appium_server = appium_server
        self.desired_caps = desired_caps
        self.wd = webdriver.Remote('http://'+appium_server+'/wd/hub', desired_caps)
        #add_cert.add_mitmproxy_certificate()
        self.wd.implicitly_wait(20)
        self.device_size = 0
        self.device_type = "iOS" if 'iphone' in desired_caps['device'].lower() else "Android"

    #----------------------------------------------------------------------------------------
    # Miscellaneous methods
    #
    def is_alert_present(self):
        try:
            self.wd.switch_to_alert().text
            return True
        except:
            return False
        
    def quit(self): 
        self.wd.quit()
     
    def relaunch(self):
        self.wd = webdriver.Remote('http://'+self.appium_server+'/wd/hub', self.desired_caps)
        
    def get_device_resolution(self):
        if self.device_size == 0:
            self.device_size = self.wd.find_element_by_xpath("//window[1]").size
        return self.device_size
       
    def execute_script(self, script, args=None):
        log.info(" ".join(["Executing script:", script, str(args)]))
        return self.wd.execute_script(script, args)

    def loading_status(self):
        """
        return boolean telling whether is still loading or finished.
        only for iOS now.
        """
        statusbar = self.wd.find_element_by_xpath('//window[2]/statusbar[1]')
        # get all elements on the status bar
        eles = statusbar.find_elements_by_xpath('*')
        # the loading element's name is "Network connection in progress"
        for ele in eles:
            #print ele.get_attribute('name')
            if "Network connection in progress" == ele.get_attribute('name'):
                return True
        try:
            self.wd.implicitly_wait(0.1)
            eles = self.wd.find_elements_by_tag_name('activityIndicator')
            self.wd.implicitly_wait(30)
            return eles[0].is_displayed()
        except:
            self.wd.implicitly_wait(30)
            return False

    def get_all_available_elements_on_current_view(self):
        pagesource = json.loads(self.get_page_source())
        elements_tree = PageSourceElementsTree(pagesource)
        nodes = elements_tree.get_all_available_elements()
        elements = []
        for node in nodes:
            xpath = node['xpath']
            elements.append(self.find_element_by_xpath(xpath))
        return elements

    #----------------------------------------------------------------------------------------
    # find element
    #
    def find_element(self, uimap_element, element_type=0):
        if element_type == 1 or str(uimap_element).startswith('//'):
            # xpath element. assume // string indicate xpath
            log.info("Finding element by xPath: " + uimap_element)
            return self.find_element_by_xpath(uimap_element)
        elif element_type == 2:
            # partial text
            log.info("Finding element by partial text: " + str(uimap_element))
            if isinstance(uimap_element, list):
                text = uimap_element[:-1]
                count = int(uimap_element[-1])
            else:
                text = uimap_element
                count = 1
            return self.find_element_by_partial_text(text, count)
        else:
            # name
            log.info("Finding element by name: " + uimap_element)
            return self.find_element_by_name(uimap_element)
        
    def find_element_by_name(self, name):
        return self.wd.find_element_by_name(name)
    
    def find_element_by_xpath(self, xpath):
        return self.wd.find_element_by_xpath(xpath)
    
    def find_element_by_partial_text(self, text, count=1):
        """
        2013.12.30

        Find an element by its partial text
        this function is with low efficiency.
        
        Parameters:
            text        : array of words
            count       : the number of the expected element  
            
        Return:
            the expected WebElement or None
        """
        pagesource = self.get_page_source()
        pagesource = json.loads(pagesource)

        "contructing the xPath for the selected node and find the"
        "webdriver element by using its xPath."
        elements_tree = PageSourceElementsTree(pagesource)
        elements = elements_tree.find_node_by_partial_text(text, count)
        if not elements:
            return False
        xpath = elements_tree.get_xpath_for_selected_node(elements)
        log.info("APPIUM_DRIVER - xPath for the element is: " + xpath)
        element = self.find_element_by_xpath(xpath)
        return element
    
    def get_page_source(self):
        """
        2013.12.30
        return the page source (string) of the views.
        """
        pagesource = self.wd.page_source
        if pagesource == '':
            pagesource = get_page_source_for_android_device()
        return pagesource

    #----------------------------------------------------------------------------------------
    # execute actions
    #
    def click(self, uimap_element, element_type=0):
        t = str(type(uimap_element)).lower()
        if 'webelement' in t:
            # wedDriver element
            element = uimap_element
        else:
            element = self.find_element(uimap_element, element_type)
        log.info("Clicking element: " + str(uimap_element))
        return element.click()
    
    def try_to_click(self, uimap_element, element_type=0):
        """
        Click the element only once.
        """
        self.wd.implicitly_wait(1)  
        try:
            log.info("Clicking element: " + uimap_element)
            self.click(uimap_element, element_type)
        except:
            self.wd.implicitly_wait(30)
            return False
        self.wd.implicitly_wait(30)
        return True
    
    def send_keys(self, uimap_element, keys, element_type=0):
        t = str(type(uimap_element)).lower()
        if 'webelement' in t:
            element = uimap_element
        else:
            element = self.find_element(uimap_element, element_type)
        log.info("Sending " + keys + " to element: " + uimap_element)
        return element.send_keys(keys)
    
    def take_screenshot(self, pic_name):
        paths = pic_name.split("/")
        path = os.getcwd()
        for t in paths[:-1]:
            path = '/'.join([path, t])
            if not os.path.exists(path):
                os.mkdir(path)
        if not pic_name.endswith(".png"):
            pic_name += '.png'
        log.info("Taking screenshot: " + pic_name)
        return self.wd.get_screenshot_as_file(pic_name)
    
    def refresh(self):
        """
        Pull and refresh. sending the script to execute.
        """
        self.return_to_top()
        return self.wd.execute_script("mobile: swipe",
                                      {"touchCount": 1, "startX": 0.5, "startY": 0.2,
                                       "endX": 0.5, "endY": 0.7, "duration": 1})
        while self.loading_status():
            print "loading"
            time.sleep(1)

    def return_to_top(self):
        """
        return to the top of list by clicking the status bar
        """
        self.wd.find_element_by_xpath("//window[2]/statusbar[1]").click()

    def move(self, direction, delta):
        d = dict(up=[0, 1], down=[0, -1], left=[1, 0], right=[-1, 0])
        
        size = self.get_device_resolution()
        
        if delta <= 1:
            delta = int(size['height'] * delta) if direction in ['up', 'down'] else int(size['width'] * delta)
            
        cx = size['width'] / 2
        cy = size['height'] / 2 - 64
        
        h = min(delta, cx * 2 - 10) if direction in ['left', 'right'] else min(delta, cy * 2 - 10)
        
        while delta > 0:
            
            hh = h/2
            param =  {
                  "touchCount" : 1,
                  "startX"     : cx + d[direction][0]*hh,
                  "endX"       : cx - d[direction][0]*hh,
                  "startY"     : cy + d[direction][1]*hh,
                  "endY"       : cy - d[direction][1]*hh,
                  "duration"   : max(0.5, 0.5*hh/200)
                  }
            self.wd.execute_script("mobile: swipe", param)
            delta -= h
            h = min(h, delta)
            time.sleep(0.5)
        return True
    
    def move_point_to_point(self, startp, endp):
        """
        Move from one position to another position
        """
        size = self.get_device_resolution()
        
        if startp[0]*startp[1] <= 1:
            startx = startp[0] * size['width']
            starty = startp[1] * size['height']
        
        if endp[0]*endp[1] <= 1:
            endx = endp[0] * size['width']
            endy = endp[1] * size['height']
             
        param = {
                  "touchCount" : 1,
                  "startX"     : startx,
                  "endX"       : endx,
                  "startY"     : starty,
                  "endY"       : endx,
                  "duration"   : 0.5
                  }
        self.wd.execute_script("mobile: swipe", param)
        
    def move_element_to_visible_area(self, element):
        """
        # scroll the element to visible area
        # according to the location and size
        """
        if element.is_displayed():
            return True
        
        location = element.location
        size = element.size
        device_size = self.get_device_resolution()

        if location['y'] > device_size['height']:
            delta = location['y'] - device_size['height'] + size['height'] + 20
            self.move('up', delta)

        if location['y'] < 0:
            delta = 40 - location['y']
            self.move('down', delta)
          
        if location['x'] > device_size['width']:
            delta = location['x'] - device_size['width'] + size['width'] + 20
            self.move('left', delta)
            
        if location['x'] < 0:
            delta = 20 - location['x']
            self.move('right', delta)
            
        return True

    def scroll_to(self, element):
        t = str(type(element)).lower()
        if 'webelement' in t:
            # webdriver element
            e = element
        else:
            # locate the element first
            e = self.find_element(element)
            if not e:
                return False

        params = {"element": e.id,
                  "text": "Views"}
        self.execute_script("mobile: scrollTo", params)

    def set_location(self, location):
        self.execute_script('mobile: setLocation', location)
        

def get_page_source_for_android_device():
    """
    2013.12.30
    If the default method fails, use this way to get page source
    """
    adb_path = "/Users/Zhenyu/Working/android-sdk-macosx/platform-tools/adb"
    cmd = adb_path + " shell uiautomator dump /data/local/tmp/dump.xml"
    os.system(cmd)
    cmd = adb_path + " pull /data.json/local/tmp/dump.xml temp.xml"
    os.system(cmd)
    f = open("temp.xml")
    t = json.dumps(xmltodict.parse(f.read()))
    f.close()
    os.remove('temp.xml')
    return t

if __name__ == "__main__":
    pass