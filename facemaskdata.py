
import cv2 as cv
import tensorflow
import numpy as np

img = cv.imread('../Downloads/masked.webp')
haar_faces_dataset = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
facemask_data = []

capture = cv.VideoCapture(0)
while True:
    ret, img = capture.read()
    if ret == True:
        faces = haar_faces_dataset.detectMultiScale(img)
        for x, y, w, h in faces:
            cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0))
            face_img = img[y:y+h, x:x+w]
            face_img = cv.resize(face_img, (60, 60))
            if len(facemask_data) < 500:
                facemask_data.append(face_img)
                print(len(facemask_data))
        cv.imshow('result',img)
        if cv.waitKey(2) == 27:
            break
    else:
        ("Camera Issues Faced")

np.save('with_mask.npy', facemask_data)
        
capture.release()
cv.destroyAllWindows()