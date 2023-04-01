import os
import shutil
from keras.preprocessing import image
from keras.applications.resnet50 import ResNet50, preprocess_input
import numpy as np

# Define the pre-trained CNN model
model = ResNet50(weights='imagenet', include_top=True)

# Define the list of categories to sort images into
categories = {
    'Portrait': ['person', 'face', 'boy', 'girl', 'man', 'woman'],
    'Sports': ['sports', 'soccer', 'football', 'basketball', 'tennis'],
    'Architectural': ['building', 'architecture', 'city', 'tower', 'skyscraper'],
    'Landscape': ['landscape', 'nature', 'mountain', 'beach', 'waterfall', 'sky'],
    'Flower': ['flower', 'plant', 'garden'],
    'Bird': ['bird', 'animal', 'feather', 'wing']
}

# Define the input and output directories
input_dir = 'path/to/input/directory'
output_dir = 'path/to/output/directory'

# Loop through each image file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # Load the image and preprocess it
        img_path = os.path.join(input_dir, filename)
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Predict the label of the image using the pre-trained model
        preds = model.predict(x)
        label = image.label_to_name(np.argmax(preds))

        # Sort the image into the appropriate category folder
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in label.lower():
                    output_path = os.path.join(output_dir, category)
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    shutil.copy(img_path, output_path)
                    break
