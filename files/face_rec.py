import cv2
import sys


imagePath = sys.argv[1]
cascPath = "/home/eyal/Desktop/adblock/files/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(3, 3),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
our = "False"
if len(faces) > 0:
    our = "True"

with open("/home/eyal/Desktop/adblock/files/to_block","w") as f:
    f.write(our)
