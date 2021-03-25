# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from imutils import paths
import numpy as np
import os

args = {'dataset':'C:/Users/BBAEK/Desktop/datasets', 'plot':"plot.png", 'model':'mask_detector.model'}


print("---Loading images---")
images = list(paths.list_images(args["dataset"]))
tr_data = []
tr_labels = []
for img in images:
	label = img.split(os.path.sep)[-2]
	tr_labels.append(label)

	image = load_img(img, target_size=(224, 224))
	image = img_to_array(image)
	image = preprocess_input(image)
	tr_data.append(image)
	

tr_data = np.array(tr_data, dtype="float32")
tr_labels = np.array(tr_labels)

tr_labels = LabelBinarizer().fit_transform(tr_labels)
print(tr_data, tr_labels)
tr_labels = to_categorical(tr_labels)
print(tr_data, tr_labels)