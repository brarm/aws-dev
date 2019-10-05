import requests

url = "https://test-api-gw-auth.auth.us-east-1.amazoncognito.com/oauth2/token"
 
payload = "grant_type=client_credentials&client_id=5q9usbn2uunrpbjo9h4celtknv&client_secret=t3pidsk30e7oruthjpcel4rjlvvoqm9fkgadtub654n3c20gt9b"
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'User-Agent': "PostmanRuntime/7.17.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "7d8c1d12-4c63-4fa7-a0e7-eece8133931d,167ba3e7-c4cb-4866-bd49-8859c669c9fa",
    'Host': "test-api-gw-auth.auth.us-east-1.amazoncognito.com",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "132",
    'Cookie': "XSRF-TOKEN=b3597dc7-297e-4e62-9b31-c01a029bc75e",
    'Connection': "keep-alive",
    'cache-control': "no-cache",
    }

response = requests.request("POST", url, data=payload, headers=headers, verify=False)

print(response.text)
