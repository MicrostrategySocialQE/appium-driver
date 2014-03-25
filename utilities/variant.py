'''
Created on May 28, 2013

@author: Zhenyu
'''

'''
vars are special strings in the templates that should be replaced
by a certain strings or value.
'''


import time 

'dictionary'
class varss:
    n_timestamp = "$(timestamp)"
    n_onedaylater = "$(onedaylater)"
    
    

'used for changing the var'
'what a fucking niubility characteristic of Python!'
vars_set = {
       
        varss.n_timestamp : str(int(time.time()))
        
        
        }

        
def change_var(var):
    '''
    used for changing the var to correct value.
    '''
    if var in vars_set:
        return vars_set[var]
    else:
        return var
