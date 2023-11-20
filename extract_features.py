import numpy as np
from scipy import ndimage as ndi
import cv2 as cv
import pandas as pd
import json
import os
from scipy.spatial.distance import euclidean
from sklearn.preprocessing import MinMaxScaler






'''
This file loops over all images in database, then create a feature vectore of gabor filters over each image.
'''


def gabor_extractor(img):

    #The spatial aspect ratio
    gamma=0.5
    #standard deviation of the Gaussian envelope
    sigma=0.56
    #theta : The orientation of the normal to the parallel stripes of Gabor function
    theta_list=[0, np.pi, np.pi/2, np.pi/4, 3*np.pi/4]
    #The phase offset of the sinusoidal function
    psi=0
    # lamda : Wavelength of the sinusoidal component
    lamda_list=[2*np.pi/1, 2*np.pi/2, 2*np.pi/3, 2*np.pi/4, 2*np.pi/5] 
    



        
    #turn image into gray scale
    img = cv.cvtColor(img , cv.COLOR_BGR2GRAY)
    
    local_energy_list=[]
    mean_ampl_list=[]
            
    for theta in theta_list:
        for lamda in lamda_list:
            kernel=cv.getGaborKernel((3,3),sigma,theta,lamda,gamma,psi,ktype=cv.CV_32F)
            fimage = cv.filter2D(img, cv.CV_8UC3, kernel)
            #computing mean amplitude
            mean_amplitude=np.sum(abs(fimage))
            mean_ampl_list.append(mean_amplitude)
            #computing local energy       
            local_energy=np.sum(fimage**2)
            local_energy_list.append(local_energy)


    #feature vector for the image
    feats = local_energy_list+mean_ampl_list
    return feats

    

