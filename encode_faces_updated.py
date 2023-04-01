# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
    help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
    help="face detection model to use: either `hog` or `cnn`")
ap.add_argument("-b", "--batch-size", type=int, default=32,
    help="batch size for processing images")
args = vars(ap.parse_args())

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

# initialize the total number of processed images
num_processed = 0

# open the output file for writing
f = open(args["encodings"], "wb")

# loop over the image paths in batches
for i in range(0, len(imagePaths), args["batch_size"]):
    # load the batch of input images and convert them from RGB
    # (OpenCV ordering) to dlib ordering (RGB)
    batch_paths = imagePaths[i:i+args["batch_size"]]
    batch_images = []
    for imagePath in batch_paths:
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        batch_images.append(rgb)

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the batch of images
    boxes = face_recognition.batch_face_locations(batch_images,
        number_of_times_to_upsample=0, model=args["detection_method"])

    # compute the facial embeddings for the faces in the batch
    encodings = face_recognition.batch_face_encodings(batch_images, boxes)

    # loop over the batch of images and facial embeddings
    for j, (imagePath, box, encoding) in enumerate(zip(batch_paths, boxes, encodings)):
        # build a dictionary of the image path, bounding box location,
        # and facial encodings for the current image
        d = {"imagePath": imagePath, "loc": box, "encoding": encoding}
        # write the dictionary to the output file
        f.write(pickle.dumps(d))

    # update the total number of processed images
    num_processed += len(batch_paths)
    print("[INFO] processed {}/{} images".format(num_processed, len(imagePaths)))

# close the output file
f.close()

