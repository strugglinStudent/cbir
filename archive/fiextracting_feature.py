def compute_gaborfilter():
    # This function is designed to produce a set of GaborFilters 
    # an even distribution of theta values equally distributed amongst pi rad / 180 degree
     
    kernels = []
    #gabor parameters for filters
    #in our case we will loop through different values of these parameters based on tamura charachterisqtiques
    ksize = 5  # The local area to evaluate
      # Larger Values produce more edges
    lambd = 10.0
  
     #building gabor filters based on tamura charachterstiques 
    for theta in range(2):
        theta = theta/4. *np.pi
        for sigma in (3,5):
            for lamda in np.arange(0,np.pi, np.pi/4.):
                for gamma in (0.05,0.5):
                    kernal=cv.getGaborKernel((ksize,ksize),sigma, theta,lamda, gamma,0,ktype=cv.CV_64F)
                    
                    kernels.append(kernal)
    return kernels




# This general function is designed to apply filters to our image then save the features in a seperate json database

def apply_filter(img,kernels):

    

    kernels = np.asarray(kernels)
    

    # First create a numpy array the same size as our input image
    newimage = np.zeros_like(img)
    
    # turn image to grayscale
    img = cv.cvtColor(img , cv.COLOR_BGR2GRAY)
      #Apply filter to image
    
     
    # we loop through the images and apply our Gabor Filter
    depth = -1 # remain depth same as original image
    feature_vector=[]

 
    for kern in kernels:  # Loop through the kernels in our GaborFilter
   

        
        imgfiltered = cv.filter2D(img, depth, kern)
        np.maximum(newimage, imgfiltered, newimage)
        
        
        
        list_1 = imgfiltered.tolist()
        

    return newimage
'''def filtreGaborFeats(image):

    filters = compute_gaborfilter()
    
    f = np.asarray(filters)  

    img = cv.cvtColor(img , cv.COLOR_BGR2GRAY)

    feature_vector=[]
    #calculating the local energy for each convolved image
    for j in range(20):
        temp = 0
        res = process(image, f[j])
        for p in range(128) :
            for q in range(128):
                temp = temp + res[p][q]*res[p][q]
        feats.append(temp)
    #calculating the mean amplitude for each convolved image	
    for j in range(20):
        temp = 0
        res = process(image, f[j])
        for p in range(128) :
            for q in range(128):
                temp = temp + abs(res[p][q])
        feats.append(temp)
 	#feat matrix is the feature vector for the image
    feats = np.array(feats)
    return feats 
'''

