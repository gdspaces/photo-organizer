import os
import shutil
import exifread

source_path = "/media/darkai/Elements/Laptop"
dest_path = "photo"

if not os.path.exists(dest_path):
    os.makedirs(dest_path)

for (directory, subdirs, allfile) in os.walk(source_path):
    for file in allfile:
        try:
            #print('filename:',file)
            file_name = os.path.join(directory,file)
            if file_name.lower().endswith(".jpg") or file_name.lower().endswith(".jpeg"):
                file_path = os.path.join(source_path, file_name)
                with open(file_path, "rb") as f:
                    tags = exifread.process_file(f)
                    date_tag = tags.get("EXIF DateTimeOriginal")
                    camera_tag = tags.get("Image Model")
                    camera_maker = tags.get("Image Make")
                    if date_tag and camera_tag:
                        date_str = str(date_tag).split()[0].replace(":", "-")
                        year, month, day = date_str.split("-")
                        camera_folder = os.path.join(dest_path, str(camera_maker)+" "+str(camera_tag))
                        year_folder = os.path.join(camera_folder, year)
                        month_folder = os.path.join(year_folder, month)
                        day_folder = os.path.join(month_folder, day)
                        if not os.path.exists(camera_folder):
                            os.makedirs(camera_folder)
                        if not os.path.exists(year_folder):
                            os.makedirs(year_folder)
                        if not os.path.exists(month_folder):
                            os.makedirs(month_folder)
                        if not os.path.exists(day_folder):
                            os.makedirs(day_folder)
                        shutil.copy2(file_path, day_folder)
        except Exception as e:
            print("Exception thrown."+str(e))
