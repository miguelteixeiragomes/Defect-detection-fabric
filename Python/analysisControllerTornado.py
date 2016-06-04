import base64
import os
import time
from PIL import Image
from io import BytesIO
from algorithm import analyser

def createImage(imgBase64):
    # Prepare file name with current timestamp
    timeStr = time.strftime("%Y%m%d-%H%M%S")
    fileName = "i-" + timeStr + ".jpg"
    # Decode base64 and save to file
    imgBuffer = Image.open(BytesIO(base64.decodestring(imgBase64)))
    imgBuffer.save(fileName, "JPEG")
    # Return file's name for reference
    return fileName

def analyseImage(fileName):
    return analyser(fileName)
#    time.sleep(0.5)
#    return False

def deleteImage(fileName):
    os.remove(fileName)
    
def convertToBase64(fileName):
    imageBase64 = base64.encodestring(open(fileName,"rb").read())
    return imageBase64


if __name__ == '__main__':
    imgBase64 = convertToBase64("test.jpg")
    fileName = createImage(imgBase64)
    print analyseImage(fileName)