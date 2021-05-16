from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

import torchvision.transforms as transforms
import torch.nn.functional as F
import cv2
import numpy as np
import os


def faceBox(frame, model):
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    model.setInput(blob)
    detections = model.forward()

    return detections


def facePoint(detections, i, h, w):
    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

    (startX, startY, endX, endY) = box.astype("int")
    (startX, startY, endX, endY) = (max(0, startX), max(
        0, startY), min(w - 1, endX), min(h - 1, endY))

    return (startX, startY, endX, endY)


def maskBox(frame, faceDetectionModel, maskModel):
    (h, w) = frame.shape[:2]
    detections = faceBox(frame, faceDetectionModel)

    faces = []
    locs = []
    preds = []

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            (startX, startY, endX, endY) = facePoint(detections, i, h, w)

            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            faces.append(face)
            locs.append((startX, startY, endX, endY))

    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskModel.predict(faces, batch_size=16)

    return (locs, preds)


def faceRecognitionBox(frame, device, faceDetectionModel, recognitionModel):
    (h, w) = frame.shape[:2]
    detections = faceBox(frame, faceDetectionModel)

    photo_path = "faces"
    image_val_path = []

    for i in os.listdir(photo_path):
        image_val_path.append(f'{photo_path}/{i}')

    embeds = []
    locs = []
    preds = []

    preprocess = transforms.Compose([
        transforms.ToPILImage(),
        # Pre-trained model uses 224x224 input images
        transforms.Resize(size=224),
        transforms.ToTensor(),
        transforms.Normalize(
            # Normalization settings for the model, the calculated mean and std values
            # mean=[0.6068, 0.4517, 0.3800],
            # for the RGB channels of the tightly-cropped VGGFace2 face dataset
            # std=[0.2492, 0.2173, 0.2082]
            mean=[0.5916, 0.5268, 0.4842],
            std=[0.2615, 0.2649, 0.2869]
        )
    ])

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            (startX, startY, endX, endY) = facePoint(detections, i, h, w)
            locs.append((startX, startY, endX, endY))

            face = frame[startY:endY, startX:endX]
            face = preprocess(face)
            face = face.unsqueeze(0)
            face = face.to(device)

            embed1 = recognitionModel(face)
            embeds.append(embed1)

    if len(embeds) > 0:
        for embed1 in embeds:
            image_distance_list = []  # predict모음
            for j in image_val_path:
                img2 = cv2.imread(j)
                img2 = img2[:, :, ::-1]

                img2 = preprocess(img2)
                img2 = img2.unsqueeze(0)
                img2 = img2.to(device)
                embed2 = recognitionModel(img2)

                image_distance = F.pairwise_distance(embed1, embed2)
                image_distance = image_distance.tolist()
                image_distance_list.append(image_distance[0])

            low_index = image_distance_list.index(min(image_distance_list))
            predict_name = image_val_path[low_index].split(
                '/')[-1].split('.')[0]  # who
            preds.append(predict_name)

    return (locs, preds)
