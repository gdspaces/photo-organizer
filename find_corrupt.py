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

for (directory, subdirs, allfile) in os.walk(source_path):
    for file in allfile:
        l = l +1
        bar.update(l)
        try:
            file_name = os.path.join(directory,file)
            #print(file_name)
            if file_name.lower().endswith(".jpg") or file_name.lower().endswith(".jpeg"):
                img = io.imread(file_name)
        except (ValueError) as e:
            os.rename(file_name,os.path.join(directory,file.split(".")[0]+'_corrupt.jpg'))
        except Exception as e:
            print("Exception thrown."+str(e))
