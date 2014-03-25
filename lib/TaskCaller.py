'''
Created on May 27, 2013

@author: Zhenyu
'''

import requests
from utilities import utility as utility
from utilities import constants as cn  # constant strings.
import copy
from utilities import variant


class TaskCaller(object):
    '''
    TaskCaller is responsible for sending out task requests.
    Make it simple. Just a http request caller.
    '''
    
    def __init__(self):
        self.data = None
        self.set_host()
    
    
    def set_task_template(self, templatefile):
        '''
        Provide the template file path and read the content.
        '''
        self.response_data = None
        self.change_map = {}
        
        self.data = utility.ReadFileToJson(templatefile)
        if self.data == None:
            print "Invalid template file. Please check it, ", templatefile
            return None
        
        'check if the request data exists.'
        if not self.data.has_key(cn.n_request):
            return None
        
        self.response_data = {}
        
        return 0
        
        
    def set_host(self, host = 'http://www1-uat.dev.alert.com:8104'):
        '''
        host is the host address of testing environment
        the default host is UAT environment.
        '''
        self.host = host + "/CMS/servlet/taskProc?"
        
        
    def __update_parameters(self, d, params):
        '''
        private function to replace parameters.
        
        0.
        Replacing all the substitute parameters.
        
        1.
        If the KEY of d is contained in params, then its value will be replaced by the value in the params.
        If the VALUE is contained as a key in the params, it will also be replaced
        e.g.
            params = {
                'key1' : 'value1',
                'key2' : 'value2'
            }
            
            d = {                                    d = {
                'key1' : 'value3',      ---->           'key1' : 'value1',    # value changed by key
                'key3' : 'key2'                         'key3' : 'value2'     # changed by value.
            }                                        }

        2.
        the second functionality of this method is to translate all the
        special variants in the value to the correct value.
        '''
        temp_d = copy.deepcopy(d)
        
        if isinstance(d, list):
            'processing every item in the list.'
            for i in range(len(d)):
                temp_d[i] = self.__update_parameters(d[i], params)
                
        elif isinstance(d, dict):
            'processing every value in the dict.'
            for key in d:
                temp_d[key] = self.__update_parameters(d[key], params)
        
                if key in params:
                    temp_d[key] = params[key]
        
        else:
            'replacing value procedure.'
            'potential risk. if there is problem. remember to check here.'
            
            temp_d = str(d)
            '-1. replacing the default values.'
            tt = temp_d.split('=')
            default = False
            if len(tt) == 2 and '$' in tt[0]:
                default = True
                temp_d = tt[0]
            
            '0. replacing the substitute.'
            for key in params[cn.n_substitute]:
                if '$' in key and key in temp_d:
                    v = params[cn.n_substitute][key]
                    if isinstance(v, list) or isinstance(v, dict):
                        temp_d = self.__update_parameters(v, params)
                    else:
                        temp_d = temp_d.replace(key, str(v))
                    default = False
                        
            '1. replacing the ordinary parameters according to the change_map.'
            for key in params:
                if '$' in key and key in temp_d:
                    temp_d = temp_d.replace(key, str(params[key]))
                    default = False
                    break
            
            '2. replacing the special variants.'
            for var in variant.vars_set:
                if var in temp_d:
                    temp_d = temp_d.replace(var, variant.change_var(var))
                    default = False
                    
            if default:
                temp_d = tt[1]
               
        return temp_d

    def update_request_parameters(self, params):
        '''
        Replace the out dated parameters with the latest ones.
        this replacement is used for previous results.
        '''
        
        '0-3. parameter substitution.'
        self.data = self.__update_parameters(self.data, params)
        
        '4. replacing the predefined parameters.'
        if params.has_key(cn.n_additional):
            self.data[cn.n_request].update(params[cn.n_additional])
            
        if self.data.has_key(cn.n_response):
            self.response_data = self.data[cn.n_response]
        
        return True

    def __update_change_map(self, content):
        '''
        replace the change_map with the updated parameters.
        the replacement is for future requests.
        the name is a little confusing, but you just need to 
        
        !!!remember this function is used for constructing the 
        change_map of this very task call.
        '''
        if not isinstance(content, dict):
            return None
        
        if self.response_data == None:
            return None
        
        for key in self.response_data:
            
            if content.has_key(key):
                self.change_map[self.response_data[key]] = content[key]
        
        
    def get_change_map(self):
        return self.change_map
    
    
    def send_request(self, template_file=None, parameters=None):
        '''
        Sending request to server and return the response data.

        2 arguments:
            0. template_file: the template file path.
            1. parameters: Parameters dictionary. contains substitution info.
        '''
        
        # setup template file if there is one.
        if template_file:
            if not self.set_task_template(template_file):
                return None, None
          
        # 0. substitute parameters.  
        if parameters:
            self.update_request_parameters(parameters)
                 
        # 1. return response of the request.
        params = self.data[cn.n_request]
        params_url = self.host + utility.CombineParams(params)
        header, response = utility.SendRequest(params_url)

        # 2. update the change_map for future requests.
        'the change_map can be directly accessed from outside,'
        'so the function only returns the header and response.'
        self.__update_change_map(response)
        
        return header, response, params_url

    def send_request_with_file(self, filename, template_file=None, parameters=None):
        # setup template file if there is one.
        if template_file:
            if not self.set_task_template(template_file):
                return None, None

        # 0. substitute parameters.
        if parameters:
            self.update_request_parameters(parameters)

        # 1. return response of the request.
        params = self.data[cn.n_request]
        params_url = self.host + utility.CombineParams(params)

        files = {"myfile": open(filename, 'rb')}
        params = {
                  'fileFieldName':'myfile'
                }
        r = requests.post(params_url, params=params, files=files)

        return r.headers, r.json(), r.url
