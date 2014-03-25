#!/usr/bin/env python
"""
This inspector is used for Appium debug.

@author: zheyang
"""
import time
import json
import logging
import os
from lib import appium_driver
from lib.appium_driver import AppiumDriver
from lib.appium_server import AppiumServer
from utilities import picture
from lib.pagesource_elements_tree import PageSourceElementsTree


class AppiumInspector(object):

    def __init__(self, config):
        # setup logger
        log = logging.getLogger("__main__")
        log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.NOTSET)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        ch.setFormatter(formatter)
        log.addHandler(ch)
        log.info("Inspector started.")

        # launch Appium server
        self.server = AppiumServer(config['cmd'])
        self.server.run()
        time.sleep(3)
        self.driver = AppiumDriver(config['desired_caps'])
        self.driver.wd.implicitly_wait(5)
        self.recording = []

        while True:
            "locate an element:"
            opt = raw_input("---------------------------------------------------------------\n"
                            "Find an element by following methods:\n"
                            #"   0. id\n"
                            "   1: name\n"
                            "   2: xpath\n"
                            "   3. partial text\n"
                            "   4. tag name\n"
                            "\n"
                            "Or execute:\n"
                            "   5. switch to webview window\n"
                            "   6. print page source\n"
                            "   7. execute script\n"
                            "   8. take screenshot\n"
                            #"   9. find all available elements and draw.\n"
                            #"   a. find all leaf nodes and draw.\n"
                            "   a. inner method.\n"
                            "   b. note down this views.\n"
                            "   c. save current script.\n"
                            "   d. command.\n"
                            "Which: "
                            )

            funcs = {
                '0': self.get_element_by_id,
                '1': self.get_element_by_name,
                '2': self.get_element_by_xpath,
                '3': self.get_element_by_partial_text,
                '4': self.get_elements_by_tagname,
                '5': self.switch_window,
                '6': self.print_page_source,
                '7': self.execute_script,
                '8': self.take_screenshot,
                '9': self.list_all_available_element,
                'b': self.note_down_view,
                'a': self.execute_inner_method,
                'c': self.output_recorded_script,
                'd': self.execute_command
            }
            element = None
            if opt in funcs:
                try:
                    element = funcs[opt]()
                except Exception, e:
                    log.error(e)
                    log.error("Element not found.")
                    continue
            else:
                self.quit_inspector()

            if not element:
                continue

            "choose an action to perform:"
            opt2 = raw_input("---------------------------------------------------------------\n"
                            "Do the following actions on this element:\n"
                            "   1: Click\n"
                            "   2: Send keys\n"
                            "   3. Scroll to it.\n"
                            "   4. print element information\n"
                            "   5. print its children\n"
                            "   6. draw element(s)\n"
                            "Input: "
                            )
            acts = {
                '1': self.click,
                '2': self.sendkey,
                '3': self.scrollto,
                '4': self.print_element_info,
                '5': self.print_children,
                '6': self.mark_elements
            }

            if opt2 in acts:
                act = acts[opt2]
                try:
                    act(element)
                except Exception, e:
                    print e
            else:
                print "Not supported."

    """ locator """
    def get_element_by_id(self):
        key = raw_input("Input element id: ")
        element = self.driver.wd.find_element_by_id(int(key))
        temp = {"element": '"%s"' % key,
                "arg": "ID",
                "done": False}
        self.recording.append(temp)
        return element

    def get_element_by_name(self):
        key = raw_input("Input element name: ")
        element = self.driver.find_element_by_name(key)

        temp = {"element": '"%s"' % key,
                "arg": "NAME",
                "done": False}
        self.recording.append(temp)

        return element

    def get_element_by_xpath(self):
        key = raw_input("Input element xpath: ")
        element = self.driver.find_element_by_xpath(key)

        temp = {"element": '"%s"' % key,
                "arg": "XPATH",
                "done": False}
        self.recording.append(temp)

        return element

    def get_element_by_partial_text(self):
        key = raw_input("The partial text is: ")
        if "," in key:
            key = key.split(',')
            key[-1] = int(key[-1])
            element = self.driver.find_element_by_partial_text(key[:-1], key[-1])
        else:
            element = self.driver.find_element_by_partial_text(key)

        temp = {"element": '"%s"' % key,
                "arg": "PARTIAL_TEXT",
                "done": False}

        if isinstance(key, list):
            temp['element'] = str(key)
        self.recording.append(temp)

        return element

    def get_elements_by_tagname(self):
        tag = raw_input("Input the tagname: ")
        elements = self.driver.wd.find_elements_by_tag_name(tag)
        print elements
        return elements

    """ executor """
    def click(self, element):
        element.click()

        temp = self.recording[len(self.recording) - 1]
        temp['action'] = "click"
        temp['done'] = True

    def sendkey(self, element):
        key = raw_input("The text is: ")
        element.send_keys(key)

        temp = self.recording[len(self.recording) - 1]
        temp['action'] = "send_keys"
        temp['arg'] = ', '.join(['"%s"' % key, temp['arg']])
        temp['done'] = True

    def execute_script(self):
        script = raw_input("Input the script: ")
        params = raw_input("Input the parameters (in Json format): ")
        params = json.loads(params)
        self.driver.execute_script(script, params)

        temp = {
            "done": True,
            "action": "execute_script",
            "arg": json.dumps(params),
            "element": '"%s"' % script
        }
        self.recording.append(temp)

    def take_screenshot(self):
        fn = raw_input("Input file name (default temp.png): ")
        if fn == '':
            fn = "temp"
        fn += ".png"
        self.driver.take_screenshot(fn)

    def list_all_available_element(self):
        elements = []

        pagesource = json.loads(self.driver.get_page_source())
        elements_tree = PageSourceElementsTree(pagesource)
        nodes = elements_tree.get_all_available_elements()
        print json.dumps(nodes)
        fn = str(int(time.time())) + ".png"

        self.driver.take_screenshot(fn)
        if self.driver.device_type == 'iOS':
            picture.resize(fn, self.driver.get_device_resolution().values())

        picture.mark_nodes(fn, nodes)
        return elements

    def print_element_info(self, elements):
        if not isinstance(elements, list):
            elements = [elements]
        for element in elements:
            print "\tid:\t\t\t", element.id
            print "\ttag_name:\t", element.tag_name
            print "\ttext:\t\t", element.text
            print "\tlocation:\t", element.location
            print "\tenabled:\t", element.is_enabled()
            print "\tdisplayed\t", element.is_displayed()
            print "\tsize\t\t", element.size
            print ""

    def scrollto(self, element):
        args = {"element": element.id}
        element.execute_script("mobile: scrollTo", args)

        temp = self.recording[len(self.recording) - 1]
        temp['action'] = "execute_script"
        temp['element'] = '"mobile: scrollTo"'
        temp['arg'] = json.dumps(args)
        temp['done'] = True

    def print_children(self, element):
        elements = element.find_elements_by_xpath("*")
        num = 0
        for element in elements:
            num += 1
            print "\nThe #%s element's information:" % str(num)
            self.print_element_info(element)

    """ utilities """
    def execute_inner_method(self):
        f = raw_input("Input the method: ")
        exec(''.join(["result = self.driver.", f]))
        print result

    def execute_command(self):
        exec(raw_input("Input the command: "))

    def compare_two_views(self, v1, v2):
        """
        Compare two views data. check if they are same.
        """
        # exactly same.
        if v1['page_source'] == v2['page_source']:
            return 1

        # compare available elements of two views.
        match_count = 0

        compare_fields = ['id', 'xpath', 'ids', 'texts']
        v2_available = v2['elements'].keys()

        for e1 in v1['elements'].values():
            best_match = 0
            match_flag = 0

            for k in v2_available:
                e2 = v2['elements'][k]
                t = 0
                for field in compare_fields:
                    if e1[field] == e2[field]:
                        t += 1
                if t > match_flag:
                    match_flag = t
                    best_match = k

            if match_flag > 0:
                v2_available.remove(best_match)
                match_count += match_flag

        similarity = float(match_count)*2/(len(v2['elements'])+len(v1['elements']))/len(compare_fields)
        if similarity > 0.7:
            # assume 70% is enough to determine two same views.
            return similarity

        # for else, they are two different views.
        return False

    def note_down_view(self):

        def get_all_from_node(node, field):
            texts = []
            for child in node['children']:
                texts += get_all_from_node(child, field)
            if not node[field]:
                return texts
            return [node[field]] + texts

        def double_size(nodes):
            for node in nodes:
                node['rect']['origin']['x'] *= 2
                node['rect']['origin']['y'] *= 2
                node['rect']['size']['width'] *= 2
                node['rect']['size']['height'] *= 2


        # get available elements from this views.
        pagesource = json.loads(self.driver.get_page_source())
        elements_tree = PageSourceElementsTree(pagesource)
        available_nodes = elements_tree.get_all_available_elements()

        nodes = {}
        id = 0

        for node in available_nodes:
            temp = {}
            temp['rect'] = node['rect']
            #temp['information'] = node
            temp['actions'] = [
                {
                    'action': '',
                    'parameter': '',
                    'directed_view': ''
                }
            ]
            temp['xpath'] = node['xpath']
            temp['id'] = node['name']
            temp['ids'] = ', '.join(get_all_from_node(node, 'name'))
            temp['texts'] = ', '.join(get_all_from_node(node, 'label'))
            nodes[id] = temp
            id += 1

        # construct this views information.
        view = {}
        view['elements'] = nodes
        view['page_source'] = json.dumps(elements_tree.hierarchy_tree)
        view['parent_view'] = ""
        tm = str(int(time.time()))
        view['id'] = tm

        # compare with existing views in the json data file.
        data_file = "views/data.json"
        if os.path.exists(data_file):
            f = open(data_file, 'r')
            data = f.read()
            f.close()
            try:
                data = json.loads(data)
            except:
                data = {}
        else:
            data = {}

        existing_flag = False
        for k in data:
            v = data[k]
            if self.compare_two_views(v, view):
                print "Seems like this views is already existing in data.json."
                opt = raw_input("This views is same with %s, correct? (y/n): " % k)
                if opt == 'y':
                    existing_flag = True
                    break

        f = open(data_file, 'w')
        if not existing_flag:
            fn = "views/" + tm + ".png"
            self.driver.take_screenshot(fn)
            if self.driver.device_type == "iOS":
                double_size(available_nodes)
            picture.mark_nodes(fn, available_nodes)
            data[tm] = view
        f.write(json.dumps(data, indent=4, sort_keys=True))
        f.close()

    def print_page_source(self):
        pagesource = self.driver.get_page_source()
        pagesource = json.dumps(json.loads(pagesource), indent=4)
        elements_tree = appium_driver.PageSourceElementsTree(pagesource)
        print json.dumps(elements_tree.hierarchy_tree, indent=4)
        ff = open('gist/pagesource.txt', 'w')
        ff.write(json.dumps(elements_tree.hierarchy_tree, indent=4))
        ff.close()
        ff = open('gist/pagesource_original.txt', 'w')
        ff.write(pagesource)
        ff.close()

    def switch_window(self):
        if self.driver.device_type == 'iOS':
            winhs = self.driver.wd.window_handles[0]
            self.driver.wd.switch_to_window(winhs)
        else:
            self.driver.wd.switch_to_window('WEBVIEW')

    def mark_elements(self, elements):
        rects = []
        if not isinstance(elements, list):
            elements = [elements]
        for element in elements:
            rect = []
            rect.append(element.location['x'])
            rect.append(element.location['y'])
            rect.append(element.size['width'])
            rect.append(element.size['height'])
            rects.append(rect)
        fn = raw_input("Input file name (default temp.png): ")
        if fn == '':
            fn = "temp"
        fn += ".png"
        picture.draw_rectangle(fn, rects)

    def output_recorded_script(self):
        fname = raw_input("Save the recorded script into (default recorded_script.py): ")
        if not fname:
            fname = "recorded_script.py"
        if not fname.endswith(".py"):
            fname += ".py"
        f = open(fname, 'w')

        f.write('\n'.join([
            '"""recorded script"""',
            'import time',
            'import os',
            'from lib.appium_driver import AppiumDriver',
            'from lib.appium_server import AppiumServer',
            '',
            "NAME = 0  # default value",
            "XPATH = 1",
            "PARTIAL_TEXT = 2",
            '',
            '',
            "def testing(config):",
            '    driver = config["driver"]',
            ''
        ]))

        # output actions
        for r in self.recording:
            if r['done']:
                s = ''.join(["    ",
                             "driver.", r['action'],
                             '(',
                             ', '.join([r[k] for k in ('element', 'arg') if k in r]),
                             ')\n'])
                f.write(s)

        f.write('\n'.join([
            '',
            'if __name__ == "__main__":',
            '    os.system("ps aux | grep -ie bin/appium | awk \'{print $2}\' | xargs kill -9")',
            '    time.sleep(1)',
            '    desired_caps = %s' % json.dumps(self.driver.desired_caps),
            '    server = AppiumServer("%s")' % ' '.join(self.server.arguments),
            '    server.run()',
            '    time.sleep(3)',
            '    driver = AppiumDriver(desired_caps)',
            '    testing({"driver": driver})',
            '    driver.quit()',
            '    server.kill()',
            ''
        ]))
        f.close()

    def quit_inspector(self):
        opt = raw_input("Not supported. Try again? y/n: ")
        if opt != 'y':
            self.driver.quit()
            self.server.kill()
            self.output_recorded_script()
            exit(0)


if __name__ == "__main__":

    configs = {
        "device": {
            'cmd': "--app /Users/Zhenyu/Desktop/temp/Trela_37_mt.app -U 256412e2b31b75f7008d92ee05862d3458c32c96 ",
            'desired_caps': {
                "newCommandTimeout": 60000,
                "device": "iphone simulator"
            }
        },

        "simulator":{
            'cmd': "--app /Users/Zhenyu/Desktop/temp/Trela_magento_test.app",
            'desired_caps': {
                "newCommandTimeout": 60000,
                "device": "iphone simulator"
            }
        },

        "android": {
            'cmd': "--app-pkg com.alert.trela.internal --app-activity com.alert.ui.activity.DispatchActivity \
                    --app /Users/Zhenyu/Working/Trela-internal-release-37-11.apk\
                    --app-wait-activity com.alert.ui.activity.LoginActivity -m --full-reset",
            'desired_caps': {
                "newCommandTimeout": 60000,
                "device": "android"
            }

        }
    }
    config = "simulator"

    AppiumInspector(configs[config])
