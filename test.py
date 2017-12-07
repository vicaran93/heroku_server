import cv2
import sys
from skimage import io

def template_matching(img, template):
    """
    Method to find template matching. Using OpenCV's function to do it. Finds
    highest correlation point in the image when convolved with the template
    and creates a bounding rectangle around the point of the template's size.
    
    Inputs:
    img - original image where we need to find template in
    template - template that is given to cv2.matchTemplate
    """
    
    res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #return min_val, min_loc
    if min_val < 0.1:
        print ('Yes')
    else:
        print ('No')
    
def read_image_server(URL):
    hdr = {'User-Agent': 'Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    
    f = io.imread(URL, headers=hdr)
    return cv2.cvtColor(f, cv2.COLOR_RGB2BGR)

def main():
    #img = read_image_server(sys.argv[1])
    #template = read_image_server(sys.argv[2])
    print(sys.argv[2]) 
    return 0
    #template_matching(img, template)

if __name__ == '__main__':
    main()
