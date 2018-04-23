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
    path_to_tmat_1 = r't_mat_1.json'
    
    # Read image/template from the database
    print (sys.argv[1])
    im = read_image_server(website+sys.argv[1])
    template = read_image_server(website+'template.jpg')
    
    # Center & Rotations
    step_rot = 0.5
    rotations = np.arange(-2.0, 2.0+step_rot, step_rot) #rotation clockwise and counter clockwise

    data = ftm.read_json(path_to_tmat_1)
    t_mats = np.array(data['t_mat'])
        
    # Run Correlation for every type of transformation
    t0 = time.time()
    ind, corr_1 = ftm.correlation_fast(im, template, t_mats)
    
    # Best results for first round
    min_center, min_degree = data['transformations'][ind]
    
    # Second iteration!
    step_rot = 0.1
    rotations = np.arange(-1.0, 1.0+step_rot, step_rot)
    centers = ftm.get_centers(min_center, 10, 1)
    t_mats, transformations = ftm.create_apt_mat(template, centers, rotations, path_to_tmat_1, False)
    
    ind, corr_2 = ftm.correlation_fast(im, template, t_mats)
    
    # Best results for second round
    min_center, min_degree = transformations[ind]
    
    # Check percentage overlap
    transformed_samples = ftm.get_transformed_pix(template, min_center, min_degree)
    overlap = np.sum( (im[transformed_samples] == 255).astype(int))
    normalizer = np.sum( (template == 255).astype(int) )
    per_overlap = overlap/float(normalizer)
    t1 = time.time()
    
    
    if corr_2 > 0.5:
        print ('Found a match!')
    else:
        print ('not a match!')
    
#    
#    im = ftm.pre_process(im)
#    template = ftm.pre_process(template)
#    
#    # Runs the template match based on set centers and rotations
#    t0 = time.time()    
#    min_center, min_degree, min_score = ftm.fast_template_match(im, template, centers, rotations)
#    t1 = time.time()
#    
#    print ("Runtime: %2.5f seconds"%float(t1-t0))
#    if min_score > 0.5:
#        print ('Found a match!; ID: %s ; Confidence Level: %1.4f%%'%(sys.argv[1], min_score*100))
#        print (min_score)
#        print (min_degree)
#        print (min_center[0], min_center[1])
#        print (center[0], center[1])
#    else:
#        print ('Not a match for ID: %s ; Confidence Level: %1.4f'%(sys.argv[1], min_score*100))
#        print (min_score)
#        print (min_degree)
#        print (min_center[0], min_center[1])
#        print (center[0], center[1])

if __name__ == '__main__':
    main()