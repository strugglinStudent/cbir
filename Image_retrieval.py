import numpy as np
import csv
from scipy.spatial.distance import euclidean
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import euclidean_distances


def run_search(query_features ):
	limit=12
	results = dict()
	path = './gabor_features.csv'

	with open(path) as f:
		reader = csv.reader(f)
		for row in reader:
				#separiting the the image Name from features, and computing the chi-squared distance.
				features = [float(x) for x in row[1:]]
				
				query_features = [float(i) for i in query_features]
				dist = euclidean(query_features,features)

				results[row[0]] = dist
				#distances[i] = dist
				#i+=1
				
		f.close()

	results = normalize(results , 25)
		
			
		#dictionarry sort
	results = sorted(
			[(v,k) for (k,v) in results.items()]
		)
	return results[:limit]


       
# normalize distances 
def normalize(distances , scale) :
       #vect = (vector - min(vector)) / (max(vector) - min(vector))*scale
       scaler = MinMaxScaler(feature_range = (0,scale))
       values = distances.values()   
       keys = distances.keys()    
       distances = np.array(list(values))
       distances = scaler.fit_transform(distances.reshape(-1 , 1 ))
       distances = dict(zip( keys , distances ))
       return distances


