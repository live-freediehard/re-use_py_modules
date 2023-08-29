import base64

str_sec=b'iR7q%9iF679-D0NT-UsE-iT-BoYYYY'

enc_sec=base64.b64encode(str_sec)

print(enc_sec)

dec_sec=base64.b64decode(enc_sec)

print(bytes.decode(dec_sec,'utf-8'))


'''
usage 
   pwd = (bytes.decode(base64.b64decode(env_cfg['SCKRT']),'utf-8')).split('-',1)[0] #decode secret!
    payload = {
        "client_id" : env_cfg['clientid'],
        "username" : env_cfg['FNAC'],
        "password" : pwd,
        "resource" : env_cfg['resource'],
'''
