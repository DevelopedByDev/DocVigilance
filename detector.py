import numpy as np
import cv2 as cv
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA

#Training
without_mask= np.load('without_mask.npy')
with_mask = np.load('with_mask.npy')

with_mask = with_mask.reshape(500, 60*60*3)
without_mask = without_mask.reshape(500, 60*60*3)

x_data = np.r_[with_mask, without_mask]
labels = np.zeros(x_data.shape[0])
labels[500:]=1.0
names = {0: "Masked", 1: "Unmasked"}

x_train, x_test, y_train, y_test = train_test_split(x_data, labels, test_size= 0.25)

pca = PCA(n_components=3)
x_train = pca.fit_transform(x_train)

svm = SVC()
svm.fit(x_train, y_train)

x_test = pca.transform(x_test)
y_pred = svm.predict(x_test)

print(accuracy_score(y_test, y_pred))

print("Detection begins now")

haar_faces_dataset = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
face_data = []
capture = cv.VideoCapture(0)
while True:
    ret, img = capture.read()
    if ret == True:
        faces = haar_faces_dataset.detectMultiScale(img)
        for x, y, w, h in faces:
            cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0))
            face_img = img[y:y+h, x:x+w, :]
            face_img = cv.resize(face_img, (60, 60))
            face_img = face_img.reshape(1, -1)
            face_img = pca.transform(face_img)
            pred = svm.predict(face_img)
            result = names[int(pred)]
            print(result)
        cv.imshow('result',img)
        if cv.waitKey(2) == 27:
            break
    else:
        ("Camera Issues Faced")
