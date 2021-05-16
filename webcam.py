from imutils.video import WebcamVideoStream
from detection import maskBox, faceRecognitionBox
from model_init import faceDetectionModel, maskModel, faceRecognitionModel


import torch
import imutils
import cv2


def startMaskDetection():
    print("[info] loading model")
    model = maskModel()
    detectionModel = faceDetectionModel()

    print("[info] starting video stream")
    vs = WebcamVideoStream().start()

    chk = [False]*30
    i = 0

    while True:
        if i > 29:
            i = 0

        frame = vs.read()
        if frame is None:
            break
        frame = imutils.resize(frame, width=1000)

        # return face points and mask prediction
        (locs, preds) = maskBox(frame, detectionModel, model)

        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (goodMask, badMask) = pred

            if goodMask > 0.5:
                label = "Good"
                color = (0, 255, 0)
                chk[i] = True
            else:
                label = "Bad"
                color = (0, 0, 255)
                chk[i] = False

            label = "{}: {:.2f}%".format(label, max(goodMask, badMask) * 100)

            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        i += 1
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or chk.count(True) > 20:
            break

    cv2.destroyAllWindows()
    vs.stop()


def startFaceRecognition() -> list:  # one person
    device = torch.device(
        "cuda") if torch.cuda.is_available() else torch.device("cpu")
    recognitionModel = faceRecognitionModel(device)
    detectionModel = faceDetectionModel()

    print("[info] starting video stream")
    vs = WebcamVideoStream().start()

    chk = []
    i = 0

    while i < 100:
        frame = vs.read()
        if frame is None:
            break
        frame = imutils.resize(frame, width=1000)

        # return face points and face recognition prediction(name)
        (locs, preds) = faceRecognitionBox(
            frame, device, detectionModel, recognitionModel)

        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box

            label = pred
            chk.append(label)
            color = (0, 255, 0)

            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        i += 1
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()

    return chk


def faceMaskDetection():  # 그래픽카드 사양 부족으로 인해 못돌림.
    print("[info] loading model")
    model = maskModel()
    detectionModel = faceDetectionModel()

    device = torch.device(
        "cuda") if torch.cuda.is_available() else torch.device("cpu")
    recognitionModel = faceRecognitionModel(device)
    detectionModel = faceDetectionModel()

    print("[info] starting video stream")
    vs = WebcamVideoStream().start()

    mask_chk = False
    while True:
        frame = vs.read()
        if frame is None:
            break
        frame = imutils.resize(frame, width=1000)

        if mask_chk:
            (locs, preds) = faceRecognitionBox(
                frame, device, detectionModel, recognitionModel)
        else:
            (locs, preds) = maskBox(frame, detectionModel, model)

        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            if mask_chk:
                label = pred
                color = (0, 255, 0)
            else:
                (goodMask, badMask) = pred
                label = "Good" if goodMask > 0.5 else "Bad"
                color = (0, 255, 0) if label == "Good" else (0, 0, 255)
                label = "{}: {:.2f}%".format(
                    label, max(goodMask, badMask) * 100)

            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()
