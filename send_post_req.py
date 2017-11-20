import requests
#from PIL import Image

# Path variables
path="C:/Users/Victor/Documents/UMass Amherst/Fall 2017/SDP/python/" #"/home/pi/Documents/access/camera/test1.jpg"
image_name="test.jpg"
final_path=path+image_name
# Load image:
#img = Image.open(final_path)
img = open(final_path)

base_url="https://sdp-lh18.herokuapp.com"
final_url=base_url+"/upload.php"
'''FIRST TRY: SUCCESSFUL
final_url=base_url+"/index_python_access_test.php"
payload = {'file_name': "from Python!"}
response = requests.post(final_url, data=payload)

print(response.text) #TEXT/HTML
print(response.status_code, response.reason) #HTTP
'''
file=img
payload = {'userfile': file}
response = requests.post(final_url, data=payload)

print(response.text) #TEXT/HTML
print(response.status_code, response.reason) #HTTP