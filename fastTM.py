import numpy as np

def SAD(im, template, center, degree):
    rows_im, cols_im = im.shape
    rows_t, cols_t = template.shape
    
    # Get white pixel locations
    samples = np.where(template >= 200)
    rad = degree*np.pi/180. 
    
    temp_im = im
    
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

def get_center(path):
    cent = path.split('/')
    cent = cent[-1]
    cent = cent.split('_')
    cent[1] = cent[1][:-4]
    cent = tuple([int(item) for item in cent])
    return cent 

def get_centers(center, search_interval):
    return [(center[0]+i, center[1]+j) for i in np.arange(-search_interval, search_interval+1, 1) for j in np.arange(-search_interval, search_interval+1, 1)]

def read_centers(path_to_centers):
    with open(path_to_centers, 'r') as f_cent:
        content = f_cent.readlines()
    
    content = [cent.strip() for cent in content]
    centers = [(int(cent.split()[0]), int(cent.split()[1])) for cent in content]
    return centers

def pre_process(im):
    im.setflags(write=1)
    im[np.where(im >= 255/2.)] = 255
    im[np.where(im < 255/2)] = 0
    return im   
    
    
    