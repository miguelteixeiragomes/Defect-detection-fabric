import base64
import os
import time
from PIL import Image
from io import BytesIO
from algorithm import analyser
# Import algorithm main Here

def createImage(sid, imgBase64):
    # Prepare file name with current timestamp
    timeStr = time.strftime("%Y%m%d-%H%M%S")
    fileName = sid + "-" + timeStr + ".jpg"
    # Decode base64 and save to file
    imgBuffer = Image.open(BytesIO(base64.decodestring(imgBase64)))
    imgBuffer.save(fileName, "JPG")
    # Return file's name for reference
    return fileName

def analyseImage(fileName):
    # return analyser(fileName) Commented until camera works
    time.sleep(0.5)
    return False

def deleteImage(fileName):
    os.remove(fileName)