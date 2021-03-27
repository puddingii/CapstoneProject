# import the necessary packages
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, AveragePooling2D, Dropout, Flatten, Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import os
args = {'dataset': 'C:/Users/BBAEK/Desktop/datasets', 'plot': "plot.png", 'model': 'mask_detector.model','plot2':"plot2.png"}

print("[info] Loading images")
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

LB = LabelBinarizer()
tr_labels = LB.fit_transform(tr_labels)
tr_labels = to_categorical(tr_labels)

(trainX, testX, trainY, testY) = train_test_split(tr_data, tr_labels,
	test_size=0.20, stratify=tr_labels, random_state=42)

aug = ImageDataGenerator(
	rotation_range=40,
	zoom_range=0.2,
	width_shift_range=0.2,
	height_shift_range=0.2,
	shear_range=0.2,
	horizontal_flip=True,
	fill_mode="nearest")


baseModel = MobileNetV2(weights="imagenet", include_top=False,
	input_shape=(224,224,3))
	#input_tensor=Input(shape=(224, 224, 3))

headModel = baseModel.output
headModel = GlobalAveragePooling2D()(headModel)
headModel = Dense(128, activation="relu")(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(2, activation="softmax")(headModel)

model = Model(inputs=baseModel.input, outputs=headModel)

for layer in baseModel.layers:
	layer.trainable = False

INIT_LR = 1e-4
EPOCHS = 10
BS = 16

print("[info] compiling model")
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

H = model.fit(
	aug.flow(trainX, trainY, batch_size=BS),
	steps_per_epoch=len(trainX) // BS,
	validation_data=(testX, testY),
	validation_steps=len(testX) // BS,
	epochs=EPOCHS
	)

print("[info] middle result")
predIdxs = model.predict(testX, batch_size=BS)
predIdxs = np.argmax(predIdxs, axis=1)
print(classification_report(testY.argmax(axis=1), predIdxs,
	target_names= LB.classes_))
with open("middle.txt", 'w') as middleFile:
	middleFile.write(classification_report(testY.argmax(axis=1), predIdxs,
	target_names= LB.classes_))

N = EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
plt.title("Middle Result")
plt.xlabel("Epoch")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot"])

#Fine-tuning
print("[info] fine-tuning")
baseModel.trainable = True

for layer in baseModel.layers:
	layer.trainable = True

fine_tune_at = 100

for layer in baseModel.layers[:fine_tune_at]:
	layer.trainable = False

print("[info] Re model compile")
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

fine_tune_epochs = 5
total_epochs =  EPOCHS + fine_tune_epochs

H = model.fit(
	aug.flow(trainX, trainY, batch_size=BS),
	steps_per_epoch=len(trainX) // BS,
	validation_data=(testX, testY),
	validation_steps=len(testX) // BS,
	epochs = total_epochs
	)

print("[info] finally result")
predIdxs = model.predict(testX, batch_size=BS)
predIdxs = np.argmax(predIdxs, axis=1)
print(classification_report(testY.argmax(axis=1), predIdxs,
	target_names= LB.classes_))
print("[INFO] saving mask detector model...")
model.save(args["model"], save_format="h5")
with open("final.txt", 'w') as finalFile:
	finalFile.write(classification_report(testY.argmax(axis=1), predIdxs,
	target_names= LB.classes_))

N = total_epochs
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
plt.title("Final Result")
plt.xlabel("Epoch")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot2"])