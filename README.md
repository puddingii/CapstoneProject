# Mask Detector & Face Recognition Model
 Detect correct wearing method & Face recognition with a mask on your face.

 Recently, wearing a mask due to the coronavirus has become mandatory, not an option. The reason for wearing a mask is that it can prevent corona infection by blocking viruses in the air.
However, if you don't wear a mask properly, the prevention effect will decrease a lot, so people should wear a mask properly. So if you enter the building, the manager at the entrance requires you to wear a mask and write a guest book, and we developed an automated machine to reduce this inconvenience.

<br>

# Dataset

턱스크 dataset
 - https://github.com/cabani/MaskedFace-Net

Face Recognition dataset
 - VGGFace2
 - LFW Dataset

<br>

# Model

턱스크

- MobileNet V2
- https://www.tensorflow.org/tutorials/images/transfer_learning?hl=ko
- http://keras-ko.kr/api/applications/mobilenet/

Face Recognition
 - Embedding : Resnet18
 - Triplet Loss
 - https://github.com/tamerthamoqa/facenet-pytorch-glint360k

<br>

# Files

Root
 - webcam.py : Run a webcam.
 - webcamMember.py : Class declaration to store recognized information.
 - model_init.py : Load the model.(face detection, mask detection, face recognition)
 - maskModel.py : Train the mask detection model.
 - detection.py : Apply the model to the webcam. And process scenes.

./front
 - visitor.py, member.py : Class to deal with visitors and members.
 - main.py : QML init.
 - qml folder, images folder : QML files and image files.
 - log folder : Information files of visitors and members.

./face_detector
 - deploy.prototxt, res10_300*300_ssd_iter_140000.caffemodel : Face detector model provided by opencv.
 - mask_detector.model : mask detector model.
 - model_resnet18_triplet_epoch_92mask.pt : face recognition model.(This is too large file)

./faceRecognition : Train the face recognition model.

./mtcnn : Resize pictures.

./resultFiles : Results of mask detection train.