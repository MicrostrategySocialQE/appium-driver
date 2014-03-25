#!/usr/bin/env python
"""
    Start up proxy server.
    In another thread.
"""
import os
from libmproxy import proxy, flow
import threading
import time
import logging
import copy

log = logging.getLogger("__main__")


class MyMaster(flow.FlowMaster):

    def __init__(self, server, state):
        flow.FlowMaster.__init__(self, server, state)
        self.flowsdata = {}
        self.request_without_response = []
        self.ever_worked = False
        self.hookups = []

    def run(self):
        log.info("Starting proxy server...")
        try:
            flow.FlowMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, request):
        f = flow.FlowMaster.handle_request(self, request)
        if f:
            request.reply()
            self.ever_worked = True
            u = f.request.host + f.request.path
            hooked = False
            for hookup in self.hookups:
                if hookup in u:
                    hooked = True
            if hooked:
                self.request_without_response.append(u)
        return f

    def handle_response(self, response):
        f = flow.FlowMaster.handle_response(self, response)
        if f:
            response.reply()
            "response returned."
            u = f.request.host + f.request.path
            if u in self.request_without_response:
                self.request_without_response.remove(u)

            "restore json flows."
            content_type = f.response.get_content_type()
            if content_type and "json" in content_type:
                self.flowsdata[len(self.flowsdata)] = f
        return f

    def has_flow_in_process(self):
        if self.ever_worked:
            if self.request_without_response:
                log.info("Proxy - " + str(self.request_without_response))
                return True
            else:
                log.info("Proxy - No flow in process.")
                return False

    def format_flows_data(self):
        ret = {}
        for i in self.flowsdata:
            f = self.flowsdata[i]
            ret[i] = {
                'request': {name: getattr(f.request, name) for name in dir(f.request)
                            if name in ['content', 'host', 'method', 'scheme', 'path']},
                'response': {name: getattr(f.response, name) for name in dir(f.response)
                             if name in ['content', 'code', 'msg']}
            }
            ret[i]['request']['headers'] = copy.deepcopy(f.request.headers['lst'])
            ret[i]['response']['headers'] = copy.deepcopy(f.response.headers['lst'])
        return ret

    def clean_flows_data(self):
        self.flowsdata = []

    def set_hookups(self, hookups=[]):
        self.hookups = hookups


class ProxySever(threading.Thread):

    def __init__(self, hookups=[]):
        threading.Thread.__init__(self)
        config = proxy.ProxyConfig(cacert=os.path.expanduser("~/.mitmproxy/mitmproxy-ca.pem"))
        state = flow.State()
        server = proxy.ProxyServer(config, 8080)
        self.proxy_master = MyMaster(server, state)
        self.proxy_master.set_hookups(hookups)
        self.setDaemon(True)

    def run(self):
        self.proxy_master.run()



if __name__ == "__main__":
    proxys = ProxySever()
    proxys.start()
    while True:
        time.sleep(5)
        print proxys.proxy_master.request_without_response
        print proxys.proxy_master.flowsdata

