import picamera
import base64
import os
import time
from PIL import Image
from io import BytesIO
import RPi.GPIO as GPIO
import io

# Init LEDs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, True)

"""
This function is responsible for capturing images
And creating the image files
Returns the file's name
"""
def capturePicture():
    # Prepare file name with current timestamp
    timestr = time.strftime("%Y%m%d-%H%M%S")
    # fileName = "i-" + timestr + ".jpg"
    fileName = "i.jpg"
    # Capture image with the Pi Camera
    # file = open(fileName, 'wb')
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(1.)
        camera.capture(fileName)
    # Close and return file's name
    # file.close()
    return fileName
    # return "test.jpg"

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
def deleteImage(fileName):
    os.remove(fileName)

def killProcess():
    # Stop ilumination
    GPIO.output(40, False)
    # Control machine here
    return True

if __name__ == "__main__":
    imgBase64Encode = convertToBase64("test.png")
    im = Image.open(BytesIO(base64.decodestring(imgBase64Encode)))
    im.save("output.png", "PNG")
