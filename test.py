import cv2
import sys
from PIL import Image
import urllib.request
import io
from skimage import io
import numpy as np

def template_matching(img, template, url1, url2):  
    try:
        res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
  
        if min_val < 0.1:
            print ('Yes', url1, url2)
            print('')
            print('')
            print('')
        else:
            print ('No', url1, url2)
            print('')
            print('')
            print('')
    except:
            print ('No', url1, url2)
            print('')
            print('')
            print('')

def read_image_server(URL):
    hdr = {'User-Agent': 'Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    
    f = io.imread(URL, headers=hdr)
    #try THIS REQUEST EVERYTIME
    #fd = urllib.request.urlopen(URL)
    #image_file = io.BytesIO(fd.read())
    #f = Image.open(image_file)
    return f.astype(np.uint8)

def main():
    
    img = read_image_server(sys.argv[1])
    template = read_image_server(sys.argv[2])

    #print(sys.argv[1], sys.argv[2]) 
    #return 0
    template_matching(img, template, sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
