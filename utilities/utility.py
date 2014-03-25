'''
Created on 25 Feb 2013

@author: zheyang
'''

'''
Includes Utilities for the project

'''
import httplib2, json, urllib, os


def SendRequest(URL, Method = 'GET'):
    '''
    Send the Request to server.
    get the response and transform them into json format.
    if cannot transform to JSON, then make them to None.
    '''
    h    = httplib2.Http()
    header, content = h.request(URL, Method)

    try:
        'content ofter encounter problem.'
        content = json.loads(content, object_hook = _decode_dict)
    except:
        content = None
        
    return header, content


def CombineParams(Params):
    '''
    Combining all parameters to a string line.
    '''
    s = ''
    for param in Params:
        value = Params[param]
        if isinstance(value, dict):
            value = json.dumps(value)
        if isinstance(value, list):
            value = str(value)
        value = value.replace('\'', '\"')
        t = '&' + param + '=' + urllib.quote(value)
        s = s + t
    return s

def ReadFileToJson(filename):
    '''
    Read a file and load its content to JSON format.
    '''
    
    f           = open(filename)
    filesize    = os.path.getsize(filename)
    data        = f.read(filesize)
    f.close()
    
    try:
        data = json.loads(data, object_hook = _decode_dict)
    except:
        print "Error while loading data to JSON: " + filename
        return None
    
    return data


def WriteJsonToFile(data, filename):
    '''
    create a new file and write the JSON data to the file.
    if the folder doesn't exit, the program will create it.
    '''
    paths = filename.split('/')
    
    d = paths[0]
    for subpath in paths[1:-1]:
        d = '/'.join([d, subpath])
        if not os.path.exists(d):
            os.mkdir(d)
            
    f = open(filename, 'w')
    s = json.dumps(data, indent =4, sort_keys=True)
    f.write(s)
    f.close()
    
    

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv   


    