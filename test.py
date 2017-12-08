import cv2
import sys
from PIL import Image
import urllib.request
import io
#from skimage import io
import numpy as np
from urllib.request import urlopen
import time

def template_matching(img, template, url1, url2):  
    try:
        res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
  
        if min_val < 0.1:
            print ('Found a Match!', url1, url2)
        else:
            print ('Nope', url1, url2)
    except:
            print ('Something went wrong', url1, url2)

def read_image_server(URL):
 #   f = io.imread(URL, headers=hdr)
    
    req = urlopen(URL)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    f = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)

    #try THIS REQUEST EVERYTIME
    #fd = urllib.request.urlopen(URL)
    #image_file = io.BytesIO(fd.read())
    #f = Image.open(image_file)
    return f

def main():
    website = "https://s3.us-east-2.amazonaws.com/access-lh18-bucket/"
    try:
        template = read_image_server(website+'template.png')
    except:
        print ("Couldn't read the template")
        return

    try:
        image_list = sys.argv[1].split()
        del image_list[0]; del image_list[1]; del image_list[2]
        
    except:
        print ('list not given properly')
        return

    try:
        t0 = time.clock()
        for link in image_list: 
            img = read_image_server(link)
            template_matching(img, template, link, website+'template.jpg')
    except:
        print ('Something went wrong in template matching')
        return

    t1 = time.clock()
    print('Average time: %2.5f'%(t1-t0)/len(image_list))

if __name__ == '__main__':
    main()
