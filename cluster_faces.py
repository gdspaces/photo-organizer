# import the necessary packages
from sklearn.cluster import DBSCAN
from imutils import build_montages
import numpy as np
import argparse
import pickle
import cv2
# importing os module
import os
 
# importing shutil module
import shutil


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-j", "--jobs", type=int, default=-1,
	help="# of parallel jobs to run (-1 will use all CPUs)")
args = vars(ap.parse_args())

dest_path = "c_faces_0.37/"
if not os.path.exists(dest_path):
    os.makedirs(dest_path)

# load the serialized face encodings + bounding box locations from
# disk, then extract the set of encodings to so we can cluster on
# them
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())
data = np.array(data)
encodings = [d["encoding"] for d in data]

# cluster the embeddings
print("[INFO] clustering...")
clt = DBSCAN(eps=0.37,min_samples=3, metric="euclidean", n_jobs=args["jobs"])
clt.fit(encodings)
# determine the total number of unique faces found in the dataset
labelIDs = np.unique(clt.labels_)
numUniqueFaces = len(np.where(labelIDs > -1)[0])
print("[INFO] # unique faces: {}".format(numUniqueFaces))


# loop over the unique face integers
for labelID in labelIDs:
	# find all indexes into the `data` array that belong to the
	# current label ID, then randomly sample a maximum of 25 indexes
	# from the set
	print("[INFO] faces for face ID: {}".format(labelID))
	idxs = np.where(clt.labels_ == labelID)[0]
	print(idxs)
	#idxs = np.random.choice(idxs, size=min(25, len(idxs)),
	#	replace=False)
	# initialize the list of faces to include in the montage
	if not os.path.exists(dest_path+"faces"+str(labelID)):
	    os.makedirs(dest_path+"faces"+str(labelID))
	# loop over the sampled indexes
	for i in idxs:
		# load the input image and extract the face ROI
		print(data[i]["imagePath"])
		file_name = os.path.basename(data[i]["imagePath"])
		dest = shutil.copyfile(data[i]["imagePath"], dest_path+"faces"+str(labelID)+"/"+file_name)
