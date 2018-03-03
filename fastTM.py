import cv2
import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time

def read_image_pil(image_name): 
    im = Image.open(image_name)
    return np.asarray(im, dtype=np.float32)

def read_image_cv(image_path): 
    im = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    #im = cv2.imread(image_path)
    return im

def rotate_image(image, center, degree):
    rows, cols = image.shape

    M = cv2.getRotationMatrix2D(center, degree, 1)
    dst = cv2.warpAffine(image,M,(cols,rows), flags= cv2.INTER_NEAREST)
    return dst

def translate_image(image, x, y):
    num_rows, num_cols = image.shape[:2]
    
    translation_matrix = np.float32([ [1,0,x], [0,1,y] ])
    dst = cv2.warpAffine(image, translation_matrix, (num_cols, num_rows))
    return dst

def SAD(im, template, center, degree):
    rows_im, cols_im = im.shape
    rows_t, cols_t = template.shape
    
    # Get white pixel locations
    samples = np.where(template >= 200)
    rad = degree*np.pi/180. 
    
    #temp_im = imrotate(im, degree)
    #temp_im = im
    temp_im = rotate_image(im, center, degree)
    
    t_mat = np.array([[np.cos(rad), -np.sin(rad), center[0] - int(rows_t/2)], [np.sin(rad), np.cos(rad), center[1] - int(cols_t/2)]])
    transformed_samples = np.around(np.dot(t_mat, np.array([samples[0], samples[1], len(samples[1])*[1]])))

    keep_mask = (transformed_samples[0][:] < rows_im-1) & (transformed_samples[0][:] > 0) & \
     (transformed_samples[1][:] < cols_im-1) & (transformed_samples[1][:] > 0)

    samples = (samples[0][keep_mask], samples[1][keep_mask])
    transformed_samples = (np.array(transformed_samples[0, keep_mask], dtype=np.int64), np.array(transformed_samples[1, keep_mask], dtype=np.int64))
    total_error = np.abs( np.subtract(template[samples], temp_im[transformed_samples] ))
    total_error = np.sum(total_error)
    
    normalizer = np.sum(template[samples])
   
    if normalizer != 0:
        sad = total_error/normalizer
    else:
        sad = 1.0

    return sad
    
    
def correlation(im, template, center, degree):
    rows_im, cols_im = im.shape
    rows_t, cols_t = template.shape
    
    # Get white pixel locations
    samples = np.where(template >= 200)
    rad = degree*np.pi/180. 
    
    
    t_mat = np.array([[np.cos(rad), -np.sin(rad), center[0] - int(rows_t/2)], [np.sin(rad), np.cos(rad), center[1] - int(cols_t/2)]])
    
    transformed_samples = np.around(np.dot(t_mat, np.array([samples[0], samples[1], len(samples[1])*[1]])))

    keep_mask = (transformed_samples[0][:] < rows_im-1) & (transformed_samples[0][:] > 0) & \
     (transformed_samples[1][:] < cols_im-1) & (transformed_samples[1][:] > 0)

    samples = (samples[0][keep_mask], samples[1][keep_mask])
    transformed_samples = (np.array(transformed_samples[0, keep_mask], dtype=np.int64), np.array(transformed_samples[1, keep_mask], dtype=np.int64))

    #mean_temp = np.mean(template[samples])
    #mean_im = np.mean(im[transformed_samples])

    correlation = np.sum( np.multiply(template[samples], im[transformed_samples] ) )
    #correlation = np.mean( np.multiply(template[samples] - mean_temp, temp_im[transformed_samples] - mean_im) )
    normalizer = np.sqrt( np.sum( np.square(template[samples]) ) * np.sum( np.square(im[transformed_samples]) ) )
    #normalizer = np.std(template[samples]) * np.std(temp_im[transformed_samples])
    
    if normalizer != 0:
        correlation = correlation/normalizer
    else:
        correlation = 0.0

    return correlation
    
def fast_template_match(im, template, centers, rotations, correlation_f=True):
    SAD_scores = {center: {round(degree, 2): np.inf for degree in rotations} for center in centers}

    for center in centers:
        for degree in rotations:
            if correlation_f is False:
                SAD_scores[center][round(degree, 2)] = SAD(im, template, center, degree)
            else:
                SAD_scores[center][round(degree, 2)] = correlation(im, template, center, degree)
                
    #min_center, min_ = max(SAD_scores.items(), key= lambda (key, val): max(val.items(), key= lambda (key2, val2): val2))
    if correlation_f is False:
        one_lvl = [(key_, min(val_.items(), key= lambda item: item[1])) for (key_, val_) in SAD_scores.items()]
        returned = min(one_lvl, key= lambda item: item[1][1]) 
        min_center, min_degree, min_score = returned[0], returned[1][0], returned[1][1]    
    else:
        one_lvl = [(key_, max(val_.items(), key= lambda item: item[1])) for (key_, val_) in SAD_scores.items()]
        returned = max(one_lvl, key= lambda item: item[1][1]) 
        min_center, min_degree, min_score = returned[0], returned[1][0], returned[1][1]  
    
    #print SAD_scores.items()
    return min_center, min_degree, min_score

def template_matching(img, template, box=False):  
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
    #res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if box:
        print ('Max val for tm = %2.5f'%max_val)
        print ("Center (row, col): (%d, %d)"%(round(max_loc[1]+h/2), round(max_loc[0]+w/2)))
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img, top_left, bottom_right, 255, 2)
        plot_image(img, template)
        
    return max_val
    
    if max_val > 0.3:
        print ('Found a Match!')
    else:
        print ('Nope')    

def plot_image(image, template):
    fig, ax = plt.subplots(nrows=1, ncols=2)
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.imshow(template, cmap='gray')
    plt.axis("off")
    plt.show()

def get_center(path):
    cent = path.split('/')
    cent = cent[-1]
    cent = cent.split('_')
    cent[1] = cent[1][:-4]
    cent = tuple([int(item) for item in cent])
    return cent 

def pre_process(im):
    im.setflags(write=1)
    im[np.where(im >= 255/2.)] = 255
    im[np.where(im < 255/2)] = 0
    return im

def get_centers(center, search_interval):
    return [(center[0]+i, center[1]+j) for i in np.arange(-search_interval, search_interval, 1) for j in np.arange(-search_interval, search_interval, 1)]

def read_centers(path_to_centers):
    with open(path_to_centers, 'r') as f_cent:
        content = f_cent.readlines()
    
    content = [cent.strip() for cent in content]
    centers = [(int(cent.split()[0]), int(cent.split()[1])) for cent in content]
    return centers
    
def main():
    #PATHS
    #path_to_centers = r"C:\Users\Hassaan\Desktop\School related\Fall 2017\SDP\Real data\ID 1/location.txt"
    #centers = read_centers(path_to_centers)
    
    path_to_image = r"C:\Users\Hassaan\Desktop\School related\Fall 2017\SDP\Database\im_1/im_1.jpg"
    path_to_template = r"C:\Users\Hassaan\Desktop\School related\Fall 2017\SDP\Database\im_1/623_748.jpg"

    path_to_image = r"C:\Users\Hassaan\Desktop\School related\Fall 2017\SDP\Real data/2018-01-29_1905_cropped_bw.jpg"
    path_to_template = r"C:\Users\Hassaan\Desktop\School related\Fall 2017\SDP\Real data/1905.jpg"
    centers = (340, 1465)
    
    #path_to_image = r"C:\Users\Hassaan\Desktop\School related\Fall 2017\SDP\Real data/2018-02-23_1805_cropped_bw.jpg"
    #path_to_template = r"C:\Users\Hassaan\Desktop\School related\Fall 2017\SDP\Real data/1805.jpg"
    #centers = (308, 614)
    
    path_to_image = r"C:\Users\Hassaan\Desktop\School related\Fall 2017\SDP\Real data\ID 1/2018-03-02_1902_cropped_bw.jpg"
    path_to_template = r"C:\Users\Hassaan\Desktop\School related\Fall 2017\SDP\Real data\ID 1/template.jpg"
    path_to_template = r"C:\Users\Hassaan\Desktop\School related\Fall 2017\SDP\Real data\ID 1/template_2.jpg"
    centers = (308, 1435)
    
    im = read_image_pil(path_to_image)
    template = read_image_pil(path_to_template)
    
    #template_matching(im, template, True)

    #ROTATIONS
    rotations = np.arange(-2, 2, 0.2) #rotation clockwise and counter clockwise
    rows_im, cols_im = im.shape
    
    #center = get_center(path_to_template)
    centers = get_centers(centers, 5)
    
    print ('Image shape:', im.shape)
    print ('Template shape:', template.shape)
    im = pre_process(im)
    template = pre_process(template)
    t0 = time.time()
    correlation_f = True
    min_center, min_degree, min_score = fast_template_match(im, template, centers, rotations, correlation_f)
    t1 = time.time()
    
    if correlation_f is False:
        print ('\n')
        print ("Min degree: %1.1f"%min_degree)
        print ("Min score: %2.4f"%min_score)
        print ("Min center: %s"%(min_center,))
        print ("Runtime: %2.5f"%float(t1-t0))
    else:
        print ('\n')
        print ("Max degree: %1.1f"%min_degree)
        print ("Max score: %2.4f"%min_score)
        print ("Max center: %s"%(min_center,))
        print ("Runtime: %2.5f"%float(t1-t0))
    
    #plt.figure()
    #plt.imshow(im, cmap='gray')    
    if min_degree != 0:
        #plt.figure()
        #plt.imshow(im, cmap='gray')  
        #im = rt.rotate_image(im, min_degree*np.pi/180., min_center[0], min_center[1] )
        template = rotate_image(template, min_center, min_degree)
        #plt.figure()
        #plt.imshow(im, cmap='gray')
        
    template_matching(im, template, True)
    
if __name__ == '__main__':
    main()
    
    

    
    
    
    
    
    
    