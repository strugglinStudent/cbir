[ Assignment-2 for Elective CSPE31 ]

# Image-Retrieval (Content-Based Image Retrieval System)

## Introduction
This repository implements `Image Search Engine` through `CBIR` (content based image retrieval) approach.
CBIR approach pays greater attention to global and local information, such as color, shape, texture, region of an image.

## Part 1. Feature Extraction

Feature extraction is a means of extracting compact but semantically valuable information from images. This information is used as a signature for the image. Similar images should have similar signatures.

In this retrieval system, i implemented several image features descriptors:

* `color-based`
    To extract the color features from the content of an image, a proper color space(HSV in this case) and an effective color  descriptor are determined through color histogram(Local color histogram). </br>
* `texture-based` 
  
  Texture can be thought of as repeated patterns of pixels over a spatial domain. Texture properties are the visual patterns     in an image that have properties of homogeneity that do not result from the presence of only a single color or intensity.
  Frequency and orientation representations of the `Gabor filter` are similar to those of the human visual system. The images     are filtered using the real parts of various different Gabor filter kernels. The mean and variance of the filtered images are   then used as features for classification, which is based on the least squared error.</br>
* `shape-based` 
   In this descriptor, feature vector is extracted by segementing image into smaller cells and for each cell, we accumulate a local histogram of gradient in several orientations over all the pixels in the cell. 
</br>

## Part 2. Indexing dataset

Now apply image descriptor to each image in your dataset, extract features from these images, and write the features to storage (ex. CSV file, RDBMS, Redis, etc.) so that they can be later compared for similarity.</br>
**color-based** - `run python3 /color/index.py --index index.csv` </br>
**texture-based** - `run python3 /gabor/index.py --index index.csv` </br>
**shape-based** - `run python3 /hog/index.py --index index.csv` </br>


## Part 3. Define Similarity metric

Depending upon dataset and types of features extracted, define a method (ex. Euclidean distance, Cosine distance, and chi-squared distance) to compare features for similarity. </br>
I used chi-squared distance for color histogram and HOG methods, Least square error technique for gabor filter method and orthogonal projection of one feature vector onto another for VGG16 method to compare similarity between features.

## Part 4. Searching

This part performs actual search of user query image by (1) extracting features from this query image and then (2) apply your similarity function to compare the query features to the features already indexed. From there, system returns the most relevant results according to your similarity function.</br>

### Results (Top 5 of each method)
**color** <br>
`run python3 search.py --query ../query_images/01.jpg --c color`
**gabor** <br>
`run python3 search.py --query ../query_images/18.jpg --c gabor`
**hog** <br>
`run python3 search.py --query ../query_images/20.jpg --c hog`

### ui
`run python3 ui.py`








