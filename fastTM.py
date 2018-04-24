import json
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


def create_apt_mat(template, centers, rotations, path, save = True):
    rads = np.array(rotations)*np.pi/180.
    rows_t, cols_t = template.shape

    # Transformation matrices
    t_mat = np.zeros( (len(centers)*len(rotations), 3, 3) )
  
    save_data = {}
    transformations = []
    # Filling out transformation matrices
    counter = 0
    for center in centers:
        for i, rad in enumerate(rads):
            
            t_mat[counter, :, :] = np.array([ [np.cos(rad), -np.sin(rad), center[0] - int(rows_t/2)], 
                                              [np.sin(rad), np.cos(rad), center[1] - int(cols_t/2)],
                                              [0, 0, 1] ])
            counter += 1
            
            transformations.append( (center, rotations[i]) )

    if save:
        save_data['t_mat'] = t_mat.tolist()
        save_data['transformations'] = transformations
        #save_json(save_data, path)
    else:
        return t_mat, transformations

    
def rotate_image(image, center, degree):
    rows, cols = image.shape

    M = cv2.getRotationMatrix2D(center, degree, 1)
    dst = cv2.warpAffine(image, M, (cols,rows), flags=cv2.INTER_NEAREST)
    return dst
   

def read_json(path):
    with open(path, 'r') as out_file:
        data = json.load(out_file)
    return data

    
def correlation(im, template, center, degree):
    rows_im, cols_im = im.shape
    rows_t, cols_t = template.shape
    
    # Get white pixel locations
    samples = np.where(template == 255)
    rad = degree*np.pi/180. 
    
    t_mat = np.array([[np.cos(rad), -np.sin(rad), center[0] - int(rows_t/2)], [np.sin(rad), np.cos(rad), center[1] - int(cols_t/2)]])
    
    transformed_samples = np.around(np.dot(t_mat, np.array([samples[0], samples[1], len(samples[1])*[1]])))

    keep_mask = (transformed_samples[0][:] < rows_im-1) & (transformed_samples[0][:] > 0) & \
     (transformed_samples[1][:] < cols_im-1) & (transformed_samples[1][:] > 0)

    samples = (samples[0][keep_mask], samples[1][keep_mask])
    transformed_samples = (np.array(transformed_samples[0, keep_mask], dtype=np.int64), np.array(transformed_samples[1, keep_mask], dtype=np.int64))

    correlation = np.sum( (im[transformed_samples] == 255).astype(int))
    normalizer = np.sqrt( np.sum( ((template[samples] == 255).astype(int))*correlation))
    
    if normalizer != 0:
        correlation = correlation/normalizer
    else:
        correlation = 0.0

    return correlation
    

def fast_template_match(im, template, centers, rotations, correlation_f=True):
    SAD_scores = {center: {round(degree, 2): 0 for degree in rotations} for center in centers}
    break_flag = False
    
    for center in centers:
        for degree in rotations:
            if correlation_f is False:
                SAD_scores[center][round(degree, 2)] = SAD(im, template, center, degree)
            else:
                SAD_scores[center][round(degree, 2)] = correlation(im, template, center, degree)
                if SAD_scores[center][round(degree, 2)] > 0.9:
                    break_flag = True
                    break
        if break_flag:
            break
        
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


def correlation_fast_pieces_main(im, template, t_mats):
    samples = np.where(template == 255)
    divisor = 1000
    limit = 1000
    if len(samples[0]) >= limit:
        
        # Limit to 8000 white pixels
        samples = (samples[0][0:limit], samples[1][0:limit])
        div = int(limit/divisor); rem = 0
    else: # Had less than 8000 pixels
        div, rem = divmod(len(samples[0]), divisor)
        div, rem = int(div), int(rem)
    
    # How many pieces of 2000 white samples we want to use
    correlation_scores = {}
    for i in range(div):
        piece_samples = (samples[0][i*divisor : (i+1)*divisor], samples[1][i*divisor : (i+1)*divisor])
        correlation_scores[i] = correlation_fast_pieces(im, t_mats, piece_samples)
        if correlation_scores[i][1] > 0.9:
            return correlation_scores[i]
    
    if rem != 0:
        piece_samples = (samples[0][i*divisor : (i*divisor)+rem], samples[1][i*divisor : (i*divisor)+rem])
        correlation_scores[i+1] = correlation_fast_pieces(im, t_mats, piece_samples)
        
    return max(correlation_scores.values(), key = lambda x: x[1])
        

def correlation_fast_pieces(im, t_mats, samples):
    rows_im, cols_im = im.shape
    
    # Get white pixel locations
    samples = np.array([samples[0], samples[1], np.array(len(samples[0])*[1])])
    
    # Transformed pixels
    transformed_samples = np.around( np.dot(t_mats, samples) )
    transformed_samples = transformed_samples[:, 0:2, :]
    transformed_samples = [ (transformed_samples[i, 0, :].astype(np.int32), transformed_samples[i, 1, :].astype(np.int32)) for i in range(transformed_samples.shape[0])]

    # Correlation calculation
    ind, correlation = max( [(i, np.sum( (im[transformed_samples[i]] == 255).astype(int) )) for i in range(t_mats.shape[0])], key= lambda k: k[1] )
    normalizer = len(samples[0])
    if correlation != 0:
        correlation /= np.sqrt(normalizer*correlation)

    return ind, correlation


def get_center(path):
    cent = path.split('/')
    cent = cent[-1]
    cent = cent.split('_')
    cent[1] = cent[1][:-4]
    cent = tuple([int(item) for item in cent])
    return cent 


def get_centers(center, search_interval, step):
    return [(center[0]+i, center[1]+j) for i in np.arange(-search_interval, search_interval+step, step) for j in np.arange(-search_interval, search_interval+step, step)]


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
    

def get_transformed_pix(template, center, degree, limit = 1000):
    rows_t, cols_t = template.shape
    
    # Get white pixel locations
    samples = np.where(template == 255)
    rad = degree*np.pi/180. 

    # Limit number of white pixels
    if len(samples[0]) > limit:
        indices = np.random.randint(0, len(samples[1]), size=limit)
        samples = (samples[0][indices], samples[1][indices])
        
    t_mat = np.array([[np.cos(rad), -np.sin(rad), center[0] - int(rows_t/2)], [np.sin(rad), np.cos(rad), center[1] - int(cols_t/2)]])

    transformed_samples = np.around(np.dot(t_mat, np.array([samples[0], samples[1], len(samples[1])*[1]])))
    transformed_samples = (np.array(transformed_samples[0, :], dtype=np.int64), np.array(transformed_samples[1, :], dtype=np.int64))
    return transformed_samples


def correlation_fast(im, template, t_mats, limit = 2500):
    rows_im, cols_im = im.shape
    rows_t, cols_t = template.shape
    
    # Get white pixel locations
    samples = np.where(template == 255)
    print (len(samples[0]))
    # Limit number of white pixels
    if len(samples[0]) > limit:
        indices = np.random.randint(0, len(samples[1]), size=limit)
        samples = (samples[0][indices], samples[1][indices])
        
    samples = np.array([samples[0], samples[1], np.array(len(samples[0])*[1])])
    
    # Transformed pixels
    transformed_samples = np.around( np.dot(t_mats, samples) )
    transformed_samples = transformed_samples[:, 0:2, :]
    transformed_samples = [ (transformed_samples[i, 0, :].astype(np.int32), transformed_samples[i, 1, :].astype(np.int32)) for i in range(transformed_samples.shape[0])]

    # Correlation calculation
    correlation = [np.sum( (im[transformed_samples[i]] == 255).astype(int) ) for i in range(t_mats.shape[0])]
    normalizer = [np.sqrt(samples.shape[1]*correlation[i]) for i in range(t_mats.shape[0])]
    
    correlation = [c/float(n) for c, n in zip(correlation, normalizer) if n != 0]

    ind, max_corr = max(enumerate(correlation), key= lambda item: item[1])
    return ind, max_corr



