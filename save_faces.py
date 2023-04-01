import cv2
import os
import shutil
import time
import progressbar
from skimage import io

# function that filters vowels
def isImageFile(filename):
    ext = ['jpg', 'jpeg', 'Jpeg', 'Jpg', 'JPG', 'JPEG']
    if (filename.split(".")[1] in ext):
        return True
    else:
        return False

widgets = [' [',
         progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
         '] ',
           progressbar.Bar('*'),' (',
           progressbar.ETA(), ') ',
          ]
  
source_path = "../photo"
dest_path = "../photo_faces"
corrupt_path = "../photo_corrupt"

if not os.path.exists(dest_path):
    os.makedirs(dest_path)

if not os.path.exists(corrupt_path):
    os.makedirs(corrupt_path)

c = 0
for root_dir, cur_dir, files in os.walk(source_path):
    filtered = filter(isImageFile, files)
    c = c + len(list(filtered))

print("Total Files : "+ str(c))
bar = progressbar.ProgressBar(max_value=(c+1), widgets=widgets).start()
l = 0

csv_file = open("../faces_map.csv", "w")
for (directory, subdirs, allfile) in os.walk(source_path):
    for file in allfile:
        l = l +1
        bar.update(l)
        try:
            file_name = os.path.join(directory,file)
            #print(file_name)
            if file_name.lower().endswith(".jpg") or file_name.lower().endswith(".jpeg"):
                img = cv2.imread(file_name)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5,minSize=(300, 300),flags = cv2.CASCADE_SCALE_IMAGE)
                i = 0
                for (x, y, w, h) in faces:
                    i = i + 1
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    faces = img[y:y + h, x:x + w]
                    cv2.imwrite(dest_path+'/'+file.split(".")[0]+'_face'+str(i)+'.jpg', faces)
                    csv_file.write(dest_path+'/'+file.split(".")[0]+'_face'+str(i)+'.jpg'+';'+file_name)
                    csv_file.write('\n')
        except Exception as e:
            print("Exception thrown."+str(e))
            #os.rename(file_name, file_name+'.corrupt')
            #shutil.move(file_name, os.path.join(corrupt_path, file))
