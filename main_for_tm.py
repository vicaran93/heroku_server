import sys
import time
import numpy as np
import fastTM as ftm
import urllib.request
from skimage import io

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
    rotations = np.arange(-1.5, 2.0, 0.5)

    center = (im.shape[0]/2, im.shape[1]/2)
    centers = ftm.get_centers(center, 100, 10)
    
    im = ftm.pre_process(im)
    template = ftm.pre_process(template)
    
    # Runs the template match based on set centers and rotations
    t0 = time.time()    
    min_center, min_degree, min_score = ftm.fast_template_match(im, template, centers, rotations)
    t1 = time.time()
    
    print ("Runtime: %2.5f seconds"%float(t1-t0))
    if min_score > 0.5:
        print ('Found a match!; ID: %s ; Confidence Level: %1.4f%%'%(sys.argv[1], min_score*100))
        print (min_score)
        print (min_degree)
        print (min_center[0], min_center[1])
        print (center[0], center[1])
    else:
        print ('Not a match for ID: %s ; Confidence Level: %1.4f'%(sys.argv[1], min_score*100))
        print (min_score)
        print (min_degree)
        print (min_center[0], min_center[1])
        print (center[0], center[1])

if __name__ == '__main__':
    main()