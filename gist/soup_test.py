__author__ = 'Zhenyu'


import suds
from suds.client import Client
wsdl_file = 'https://store-demo.alert.com/api/v2_soap?wsdl=1'
user = 'hqmagento'
password = 'hqmagento123'
client = Client(wsdl_file) # load the wsdl file
session = client.service.login(user, password) # login and create a session
print session
#print client.service.catalogProductList(session)


data = {
    "website_id": 1,
    "balance": 10,
    "status": 1,
    "is_redeemable": 1
}
#print client.service.giftcardAccountCreate(session, data)

t = client.service.giftcardAccountInfo(session, "409")

print t