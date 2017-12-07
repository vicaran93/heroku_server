import requests,sys
#from PIL import Image

'''
 Input is the name without extension (useful for RPi process)
'''

# Path variables
path="C:/Users/Victor/Documents/UMass Amherst/Fall 2017/SDP/python/" #"/home/pi/Documents/access/camera/test1.jpg"

if len(sys.argv) == 2:
    image_name=sys.argv[1]+".jpg" #"test.jpg" in laptop or "test1_cropped.jpg" in RPi
    print("Seding: "+image_name)
else:
    print("No input detected in compare.py...using test.jpg as image name")
    image_name="test.jpg"
final_path=path+image_name
# Load image:
#img = Image.open(final_path)
img = open(final_path,'rb')

base_url="https://sdp-lh18.herokuapp.com"
final_url=base_url+"/compare.php"

with open(final_path, 'rb') as f: response = requests.post(final_url, files={'userfile': f})

print(response.text) #TEXT/HTML
print(response.text[0]+response.text[1])
if response.text[0] == "I": # Image received...
    print("We got response back. Show green LED!")
elif response.text[0] == "E": # Eror detected...
    print("Got an error. Show red LED!")
print(response.status_code, response.reason) #HTTP