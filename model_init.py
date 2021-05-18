from tensorflow.keras.models import load_model
from face_detector.resnet import Resnet18Triplet

import cv2
import os
import torch


def faceDetectionModel():
    print("[info] loading face detection model")
    prototxtPath = os.path.sep.join(["face_detector", "deploy.prototxt"])
    weightsPath = os.path.sep.join(
        ["face_detector", "res10_300x300_ssd_iter_140000.caffemodel"])
    model = cv2.dnn.readNet(prototxtPath, weightsPath)

    return model


def maskModel():
    print("[info] loading mask detection model")
    return load_model(os.path.sep.join(
        ["face_detector", "mask_detector.model"]))


def faceRecognitionModel(device):
    print("[info] loading face recognition model")

    checkpoint = torch.load(
        'face_detector/model_resnet18_triplet_epoch_92mask.pt', map_location=device)
    model = Resnet18Triplet(
        embedding_dimension=checkpoint['embedding_dimension'])
    model.load_state_dict(checkpoint['model_state_dict'])

    model.to(device)
    model.eval()

    return model
