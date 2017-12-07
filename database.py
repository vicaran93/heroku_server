import matplotlib.pyplot as plt
import numpy as np
import cv2
import random, os
import time, sys
from collections import defaultdict
import json

#IDEA
# Do a voting system out of 5 templates from original image.
# If 3 of them are in the image then yes? else no?
# Or template within a template? Not sure if this is necessary

def read_image(image_name): 
    """
    OpenCV defaults to BGR when it reads an image. The second line swaps blue 
    and red channels otherwise colors will be flipped.
    
    Input:
    image_name - name of image in the global path defined below
    
    Output:
    image that has Blue and Red channels swapped due to OpenCV's default properties
    """
    #os.path.join(image_path, image_name, image_name+'.png')
    im = cv2.imread(image_name)
    return cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    

def read_template(folder, template_name): 
    """
    OpenCV defaults to BGR when it reads an image. The second line swaps blue 
    and red channels otherwise colors will be flipped.
    
    Input:
    image_name - name of image in the global path defined below
    
    Output:
    image that has Blue and Red channels swapped due to OpenCV's default properties
    """
    im = cv2.imread(os.path.join(image_path, folder, template_name))
    return cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

def extract_template(image, folder_name):
    """
    This function extracts a template for testing given an image. Template size
    will be hard-coded. Template will be taken from a rectangle in the middle
    as opposed to anywhere from the entire image
    
    Input:
    image - where template will be extracted from
    
    Output:
    template - 
    """
    x = random.randint(513, image.shape[0]-513)
    y = random.randint(513, image.shape[1]-513)
    #x = int(image.shape[0]/2)
    #y = int(image.shape[1]/2)
    template = image[x-256:x+256 , y-256:y+256, :]
    name = str(x)+'_'+str(y)+'.png'
   # print name
    cv2.imwrite(os.path.join(image_path, folder_name, name), cv2.cvtColor(template, cv2.COLOR_RGB2BGR))
    
def plot_image(image):
    plt.figure()
    plt.imshow(image)
    plt.axis("off")
    
def save_image(image, im_num=0):
    if not os.path.exists(os.path.join(image_path, 'im_%d' %im_num)):
        os.makedirs(os.path.join(image_path, 'im_%d' %im_num))
        
    cv2.imwrite(os.path.join(image_path, 'im_%d' %im_num, 'im_%d.png' %im_num), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    
def template_matching(img, template):
    """
    Method to find template matching. Using OpenCV's function to do it. Finds
    highest correlation point in the image when convolved with the template
    and creates a bounding rectangle around the point of the template's size.
    
    Inputs:
    img - original image where we need to find template in
    template - template that is given to cv2.matchTemplate
    """
    
    w, h = template.shape[1], template.shape[0]
    res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #return min_val, min_loc
    if min_val < 0.1:
        print ('Yes')
        return min_val
    else:
        print ('No')
        return min_val
    
    #center = (int(min_loc[0]+w/2), int((min_loc[1]+h)/2))
    #print min_val, center
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, (255, 255, 255), 2)
    #save_image(img, 2020)
    plot_image(img)
    
image_path = r"C:\Users\SDP\Documents\Database"

def create_image(num, radius, num_of_circles):
    image_size = (2448, 3264, 3)
    img = np.zeros(image_size, np.uint8)
    for i in range(num_of_circles):
        cv2.circle(img, (random.randint(0, image_size[1]), random.randint(0, image_size[0])), random.randint(radius-1, radius+1), (155,0,0), -1)
    #plot_image(img)
    save_image(img, num)
    
    for num_t in range(1):
        extract_template(img, 'im_%d' %num)

def read_image_server(URL):
    hdr = {'User-Agent': 'Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    
    from skimage import io
    f = io.imread(URL, headers=hdr)
    return cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
    #cv2.imwrite(r"C:\Users\SDP\Documents/cucho.jpg", cv2.cvtColor(f, cv2.COLOR_RGB2BGR))
    
def main():
    rads, num_of_circles, num_of_images = 4, 2000, 300
   # test = json.load(open(r'C:\Users\SDP\Documents\Database/result.txt'))   
    
    img = read_image_server(sys.argv[1])
    template = sys.argv[2] 
    
    min_val = template_matching(img, template)

    create_images = False
    if create_images:
        for num in range(1, num_of_images+1):
            create_image(num, rads, num_of_circles)
   
    template = False
    if template:
        img_name = 'im_1'
        img = read_image(os.path.join(image_path, img_name, img_name+'.png'))
        result = []
        for size in range(3, 15):
            kernel = np.ones((size, size),np.float32)/(size*size)
            img = cv2.filter2D(img, -1, kernel)
            template = read_template(img_name, '1035_1827.png')
            result.append(1-template_matching(img, template))
        
        plt.plot([size for size in range(3, 15)], result, 'g*--')
        plt.title('Kernel size vs scoring system')
        plt.xlabel('Sizes of kernel')
        plt.ylabel('Squared diff norm coeff')
        #num_rows, num_cols = img.shape[:2]
        #translation_matrix = np.float32([ [1,0,70], [0,1,110] ])
        #img = cv2.warpAffine(img, translation_matrix, (num_cols, num_rows))
        sys.exit()
        
    template_size = False
    save_json = False
    if template_size:
        matches_dict = defaultdict(int)
        timing_dict = defaultdict(list)
        
        img_name = 'im_1'
        template = read_template(img_name, '1035_1827.png')
        
        for number_shrink in range(9):
            print ('Iteration: %d'%int(number_shrink+1))
            number_of_matches = 0
            w, h = template.shape[1], template.shape[0]
            if number_shrink != 0:
                template = template[0:w-50, 0:h-50, :]
            
            for folder in os.listdir(image_path):
                #print (folder)
                img = read_image(folder)
                t0 = time.clock()
                result = template_matching(img, template)
                t1 = time.clock()
                timing_dict[number_shrink].append(t1-t0)
                number_of_matches += result
                
            matches_dict[number_shrink] = number_of_matches             
    
        averages = [sum(vals)/len(vals) for (size, vals) in timing_dict.items()]
        print (averages)
        
        if save_json:
            file2 = open(r'C:\Users\SDP\Documents/result.txt', 'w')
            json_dict = {}
            json_dict['average times'] = averages; json_dict['matches'] = matches_dict
            json.dump(json_dict, file2)
            file2.close()

        #plotting
        plt.figure()
        plt.plot(matches_dict.keys(), matches_dict.values(), 'b*--')
        plt.xlabel('Size of template')
        plt.ylabel('Number of matches')
        plt.show()
        
        plt.figure()
        plt.plot([512-(size*50) for size in timing_dict.keys()], averages, 'r*--')
        plt.xlabel('Size of template')
        plt.ylabel('Average time')
        plt.show()
        
        
if __name__=='__main__':
    main()

