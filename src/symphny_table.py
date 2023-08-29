#!/usr/bin/python

import json, os, requests, getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Update these variables with the values for your application
# baseurl="https://verumapi-uat.jpmchase.net/Verum/6.0/api/"
baseurl="https://cisymphony.gaiacloud.jpmchase.net/restapi/rs/publish/"
#objurl = baseurl 
tokenurl = "https://ida.jpmorganchase.com/adfs/oauth2/token"
clientid = "PC-102060-G004769-142314-PROD"
resource = "JPMC:URI:RS-90623-12460-CISYMPHONY-PROD"

token_file = "./symphony_api_token.txt"

#############
# Get Auth Token
#############
def gettoken():
    #user = input("Please enter FID (Eg: AD\FID): ")
    #pwd = getpass.getpass()
    user = "AD\XXXXX" #input("Please enter FID (Eg: AD\FID): ")
    pwd = "XXXXX" #getpass.getpass()
    payload = {
        "client_id" : clientid,
        "username" : user,
        "password" : pwd,
        "resource" : resource,
        "grant_type" : "password"}

    #print("INFO: Payload:", payload)
    r = requests.get(tokenurl, data=payload)
    print("INFO: Token Call Status:", r.status_code)
    if r.status_code != 200:
        print("ERROR: Token Call failed", r.text)
        exit(1)

    accesstoken= r.json().get('access_token')
    print("INFO: Token Call Response:", r.json())
    return accesstoken


#############
# Use Token/ headers for API call
#############
def returnheaders(access_token):
        headers = {
                     "Authorization": "Bearer " + access_token,
                     "Content-Type": "application/json"
                  }
        return headers


#############
# MAIN
#############
if os.path.isfile(token_file):
   print("INFO: Reading token file:", token_file)
   inF = open(token_file, "r")
   access_token = inF.read().rstrip('\n')
   inF.close()
else:
   print("INFO: Creating token file:", token_file)
   access_token = gettoken()
   outF = open(token_file, "w")
   outF.write(access_token)
   outF.close()

headers = returnheaders(access_token)
print("INFO: API Call Header:", headers)

#payloadmsg = {
#        "messageType": "Room",
#        "recipients": ["test123456789"],
#        "messageText": "<a href=\"https://www.google.com\"> Mozilla </a>"
#        }
        
payloadmsg = {
        "messageType": "Room",
        "recipients": ["test123456789"],
        "messageText": "<table><tr><th>Person 1</th><th>Person 2</th></tr><tr><td>Emil</td><td>Tobias</td></tr><tr><td>14</td><td>10</td></tr></table>"
        }

        

#json_string = json.loads(payloadmsg)
json_string_n = json.dumps(payloadmsg)       
print(json_string_n) 
r = requests.post( baseurl, json_string_n,headers=headers, verify=False)
print("INFO: API Call Status:", r.status_code)
if r.status_code == 401:
   print("WARNING: Token Expire or unauthorized. Retrying with a new auth call...", r.text)
   access_token = gettoken()
   outF = open(token_file, "w")
   outF.write(access_token)
   outF.close()
   headers = returnheaders(access_token)
   print("INFO: API Call2 Header:", headers)
   r = requests.post( baseurl, json_string_n,headers=headers, verify=False)
   print("INFO: API Call2 Status:", r.status_code)

print("INFO API Call Response:\n", r.text)
