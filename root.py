from tensorflow.keras.backend import clear_session
from numba import cuda
from webcamMember import Member
from webcam import startMaskDetection, startFaceRecognition
from collections import Counter
import time
import torch


def getModeValue(predList):
    c = Counter(predList)
    mode = c.most_common(1)
    return mode[0][0]


if __name__ == '__main__':
    startMaskDetection()
    cuda.select_device(0)
    cuda.close()

    predList = startFaceRecognition()
    torch.cuda.empty_cache()

    memberText = "./front/frontProject/log/member.txt"
    visitorText = "./front/frontProject/log/visitor.txt"
    nowTime = time.strftime("%Y-%m-%d_%p%I:%M", time.localtime(time.time()))

    predName = getModeValue(predList)

    m = Member(memberText)
    memberList = m.get_member_list

    predMember = dict()
    for member in memberList:
        if member["NAME"] == predName:
            predMember = member
            break
    print(predMember)
    with open(visitorText, 'a', encoding='UTF-8') as file:
        file.write("{} {} {} {}\n".format(
            predMember["NAME"], nowTime, predMember["PHONE"], predMember["ADDRESS"]))
