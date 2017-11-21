import requests
import sys

'''
 Image name should be pass through console i.e sys.argv[1]
'''

# Path variables
path="C:/Users/Victor/Documents/UMass Amherst/Fall 2017/SDP/python/" #"/home/pi/Documents/access/camera/test1.jpg"
image_name=sys.argv[1] #"test.jpg"
final_path=path+image_name
# Load image:
#img = Image.open(final_path)
img = open(final_path,'rb')

base_url="https://sdp-lh18.herokuapp.com"
final_url=base_url+"/upload.php"

with open(final_path, 'rb') as f: response = requests.post(final_url, files={'userfile': f})
print(response.text) #TEXT/HTML
if response.text == "Upload successful":
    print("We got response back. File is uploaded!")
    #show green LED
elif  response.text == "Upload error":
    print("Upload error detected")
    #show red LED
else: print("No reponse detected")

print(response.status_code, response.reason) #HTTP