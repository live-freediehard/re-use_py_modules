from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File


settings = {
    'url': 'https://sp.jpmchase.net/sites/spysfdfh/SitePages/Home.aspx',
    'user_credentials': {
        'username': 'AD\g004769',
        'password': ''
    }
}

ctx_auth = AuthenticationContext(url=settings['url'])
ctx_auth.acquire_token_for_user(username=settings['user_credentials']['username'],password=settings['user_credentials']['password'])   
#ctx = ClientContext(url, ctx_auth)


'''
response = File.open_binary(ctx, "/Shared Documents/User Guide.docx")
with open("./User Guide.docx", "wb") as local_file:
    local_file.write(response.content)
Upload a file

ctx_auth = AuthenticationContext(url)
ctx_auth.acquire_token_for_user("G004769", "iR7q%9iF")   
ctx = ClientContext(url, ctx_auth)

path = "./User Guide.docx" #local path
with open(path, 'rb') as content_file:
   file_content = content_file.read()
target_url = "/Shared Documents/{0}".format(os.path.basename(path))  # target url of a file 
File.save_binary(ctx, target_url, file_content) # upload a file

'''
