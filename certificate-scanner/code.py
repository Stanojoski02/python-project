
import cv2
import numpy as np
from pyzbar.pyzbar import decode

#img = cv2.imread("img.png")
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
z = 0

while True:
    succes,img = cap.read()

    for bar in decode(img):
        myData = bar.data.decode("utf-8")
        if "https://api.zdravstvo.gov.mk/Covid19VaccineCertificates/" in myData:
            print("Sertifikato e tocen")
            z=1
        else:
            print("Sertifikato e lazen")
            z=2
        print(myData)
        pts = np.array([bar.polygon], np.int32)
        pts= pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)
        pts2 = bar.rect
        if z == 1:
            cv2.putText(img,"[+] Sertifikato e tocen",(50,50),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0),2,cv2.LINE_AA)

        else:
            cv2.putText(img, "[-] Lazen sertifikat ajde vzatvor!! :(",(50,50),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255),2,cv2.LINE_AA)
    cv2.imshow("result",img)
    cv2.waitKey(1)

