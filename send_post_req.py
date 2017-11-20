import requests

base_url="www.server.com"
final_url=base_url+"/server/index_python_access_test.php"

payload = {'number': 2, 'value': 1}
response = requests.post(final_url, data=payload)

print(response.text) #TEXT/HTML
print(response.status_code, response.reason) #HTTP