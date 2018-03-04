import sys
import numpy as np
import time
from skimage import io
import fastTM as ftm
import urllib.request

def read_image_server(URL):
    f = io.imread(URL)
    return f

def read_center(URL):
    for line in urllib.request.urlopen(URL):
        item = line.split()
    center = (int(item[0]), int(item[1]))
    return center
        
def main():
    assert(len(sys.argv) == 2)
    # Where the database is
    website = "https://s3.us-east-2.amazonaws.com/access-lh18-bucket/"
    
    im = read_image_server(website+sys.argv[1])
    template = read_image_server(website+'template.jpg')
    
    # Center & Rotations
    rotations = np.arange(-2, 2, 0.5)
    center = read_center(website+'location.txt')
    centers = ftm.get_centers(center, 2)
    
    # Runs the template match based on set centers and rotations
    t0 = time.time()    
    min_center, min_degree, min_score = ftm.fast_template_match(im, template, centers, rotations)
    t1 = time.time()
    
    print ("Runtime: %2.5f seconds"%float(t1-t0))
    if min_score > 0.5:
        print ('Found a match!')
        print ('ID: %s ; Confidence Level: %1.4f%%'%(website+sys.argv[1], min_score*100))
    else:
        print ('Not a match for ID: %s ; Confidence Level: %3.4f'%(website+sys.argv[1], min_score))
    

if __name__ == '__main__':
    main()