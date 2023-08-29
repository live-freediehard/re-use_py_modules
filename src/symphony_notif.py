#!/usr/bin/python

import json, os, requests, getpass
import pandas as pd
from io import StringIO 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

baseurl="https://cisymphony.gaiacloud.jpmchase.net/restapi/rs/publish/"
tokenurl = "https://ida.jpmorganchase.com/adfs/oauth2/token"
clientid = "PC-102060-G004769-142314-PROD"
resource = "JPMC:URI:RS-90623-12460-CISYMPHONY-PROD"
snow_url_base="https://jpmorganchase.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number="
link = "https://glcm-cgr-snow-api.apps.mt-d9.belv.gkp.jpmchase.net/api/incidents/state/open?ag=CIB_BWP_ASUP_CCMGlasIntEMEA:%20Technician&ag=CIB_BWP_ASUP_CCMEMEACash:%20Technician&ag=CIB_BWP_ASUP_CCMIDLPosition:%20Technician&ag=CIB_BWP_ASUP_CCMGlassPlatSvcs:%20Technician&ag=CIB_BWP_ASUP_CCMLiquidity:%20Technician&ag=CIB_BWP_ASUP_CCMGlassVAM:%20Technician&ag=CIB_BWP_ASUP_GLASSGLE"
token_file = "./symphony_api_token.txt"

#############
# Get Auth Token
#############

######  https://confluence.prod.aws.jpmchase.net/confluence/pages/viewpage.action?pageId=573442771

def gettoken():
    user = "AD\XXXXX" #input("Please enter FID (Eg: AD\FID): ")
    pwd = "XXXXXX" #getpass.getpass()
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

f = requests.get(link)
csvStringIO = StringIO(f.text)
df = pd.read_csv(csvStringIO, sep=",")
df_un = df[pd.isna(df["Assigned To"])]
df_srt = df.sort_values(by=['Incident #'])
df_old = df_srt.iloc[0:10, ]
str1=""
str2=""
for ind in df_un.index:
    str1=str1+"<tr><td><a href=\""+snow_url_base+str(df_un['Incident #'][ind])+"\">"+str(df_un['Incident #'][ind])+"</a>"+"</td><td>"+str(df_un['Configuration Item'][ind])+"</td><td>"+str(df_un['Description'][ind])+"</td></tr>"
for ind2 in df_old.index:
    str2=str2+"<tr><td><a href=\""+snow_url_base+str(df_old['Incident #'][ind2])+"\">"+str(df_old['Incident #'][ind2])+"</a>"+"</td><td>"+str(df_old['Configuration Item'][ind2])+"</td><td>"+str(df_old['Description'][ind2])+"</td></tr>"
msg1="<table><tr><th>Unassigned Incident#</th><th>Config Item</th><th>Description</th></tr>"+str1+"</table>"
msg2="<table><tr><th>Oldest 10 Incident#</th><th>Config Item</th><th>Description</th></tr>"+str2+"</table>"
        
payloadmsg1 = {
        "messageType": "Room",
        "recipients": ["test123456789"],
        "messageText": msg1
        }

payloadmsg2 = {
        "messageType": "Room",
        "recipients": ["test123456789"],
        "messageText": msg2
        }
        

#json_string = json.loads(payloadmsg)
json_string_1 = json.dumps(payloadmsg1)       
r = requests.post( baseurl, json_string_1,headers=headers, verify=False)
print("INFO: API Call Status:", r.status_code)


json_string_2 = json.dumps(payloadmsg2)       
r = requests.post( baseurl, json_string_2,headers=headers, verify=False)
print("INFO: API Call Status:", r.status_code)
