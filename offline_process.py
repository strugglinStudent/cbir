import cv2 as cv
import numpy as np
from pathlib import Path
import pandas as pd
import os


from extract_features import gabor_extractor



if __name__ == "__main__":

    output_file = './features.csv'
    c = 1
    all_files = os.listdir('./BE/') 
    

	#loop through images and extract features
    for img_path in sorted(Path("./BE/").glob('*.png')):
        #imageId = img_path[img_path.rfind("/")+1:]
        image = cv.imread(img_path.as_posix())

        features = gabor_extractor(image)
        features = [str(f) for f in features]
		# print("c = {}".format(c))
        c += 1
        with open(output_file, 'a', encoding="utf8") as f:
            f.write("%s,%s\n" % (img_path, ",".join(features)))
            f.close()
    

    
        




    


           