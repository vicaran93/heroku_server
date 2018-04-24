import sys
import time
import numpy as np
import fastTM as ftm
from skimage import io


def read_image_server(URL):
    f = io.imread(URL)
    return f

def main():
    assert(len(sys.argv) == 2)
    # Where the database is
    website = "https://s3.us-east-2.amazonaws.com/access-lh18-bucket/"
    path_to_tmat_1 = r't_mat_1.json'
    
    # Read image/template from the database
    try:
        im = read_image_server(website+sys.argv[1])
        template = read_image_server(website+'template.jpg')
    except:
        print ('Searched for: %s'%sys.argv[1])
        print ('Image or template not there')
        return
    
    im = ftm.pre_process(im)
    template = ftm.pre_process(template)
    rows_im, cols_im = im.shape
    rows_t, cols_t = template.shape
    
    template = template[rows_t/4:3*rows_t/4, cols_t/4:3*cols_t/4].copy()
    
    center = (im.shape[0]/2, im.shape[1]/2)
    
    # Read first set of transformations
    data = ftm.read_json(path_to_tmat_1)
    t_mats = np.array(data['t_mat'])
        
    # First iteration!
    t0 = time.time()
    ind, corr_1 = ftm.correlation_fast_pieces_main(im, template, t_mats)
    
    print ('Total: %d'%(len(data['transformations'])))
    # Best results for first round
    min_center_1, min_degree_1 = data['transformations'][ind]
    
    # Second iteration!
    step_rot = 0.1
    rotations = np.arange(-0.5+min_degree_1, 0.5+min_degree_1+step_rot, step_rot)
    centers = ftm.get_centers(min_center_1, 5, 1)
    t_mats, transformations = ftm.create_apt_mat(template, centers, rotations, path_to_tmat_1, False)
    
    print ('Second round of centers: %d; Rotations: %d; Total: %d'%(len(centers), len(rotations), len(centers)*len(rotations)) )
    
    ind, corr_2 = ftm.correlation_fast_pieces_main(im, template, t_mats)
    # Best results for second round
    min_center_2, min_degree_2 = transformations[ind]
    
    t1 = time.time()
    
    print ('')
    print ("Degree 1: %1.1f; Degree 2: %1.1f"%(min_degree_1, min_degree_2))
    print ("First round: %1.5f; Second round: %1.5f"%(corr_1, corr_2))
    print ("Center 1: (%d, %d); Center 2: (%d, %d)"%(min_center_1[0], min_center_1[1], min_center_2[0], min_center_2[1]))
    print ("Translation 1: (%d, %d); Translation 2: (%d, %d)"%(abs(center[0]-min_center_1[0]), abs(center[1]-min_center_1[1]), abs(center[0]-min_center_2[0]), abs(center[1]-min_center_2[1]) ) )
    print ("Runtime: %2.5f"%float(t1-t0))
    

if __name__ == '__main__':
    main()