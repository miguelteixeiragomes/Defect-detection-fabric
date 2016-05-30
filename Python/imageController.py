import base64
import os
import time
import picamera
# Delete these modules after testing
from PIL import Image
from io import BytesIO

"""
This function is responsible for capturing images
And creating the image files
Returns the file's name
"""
def capturePicture():
    # Prepare file name with current timestamp
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fileName = "i-" + timestr + ".jpg"
    # Capture image with the Pi Camera
    file = open(fileName, 'wb')
    with picamera.PiCamera() as camera:
        camera.capture(file)
    # Close and return file's name
    file.close()
    return fileName

"""
This function converts an image to it's
Respective base64 encoded String
"""
def convertToBase64(fileName):
    imageBase64 = base64.encodestring(open(fileName,"rb").read())
    return imageBase64

"""
This function deletes an image
"""
def deleteFile(fileName):
    os.remove(fileName)

def killProcess():
    # Control machine here
    return True

if __name__ == "__main__":
    imgBase64Encode = convertToBase64("input.png")
    im = Image.open(BytesIO(base64.decodestring(imgBase64Encode)))
    im.save("output.png", "PNG")