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
    # process_eval = multiprocessing.Process(target=startMaskDetection)
    # process_eval.start()
    # process_eval.join()
    startMaskDetection()
    cuda.select_device(0)
    cuda.close()

    predList = startFaceRecognition()
    torch.cuda.empty_cache()

    memberText = "C:/Users/BBAEK/Desktop/capstone_1/front/frontProject/log/member.txt"
    visitorText = "C:/Users/BBAEK/Desktop/capstone_1/front/frontProject/log/visitor.txt"
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
