import libjevois as jevois
import cv2
import numpy as np
import json


class Vision:

    def __init__(self):
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        # self.hsv_low = np.array([86, 40, 200])
        # self.hsv_high = np.array([90,230,255])
        # self.hsv_low = np.array([70, 90, 130])
        # self.hsv_high = np.array([85,255,255])
        # self.hsv_low = np.array([75, 50, 120])
        # self.hsv_high = np.array([90,255,255])
        # self.hsv_low = np.array([85, 40, 200])
        # self.hsv_high = np.array([90,230,255])
        self.hsv_low = np.array([70, 100, 100])
        self.hsv_high = np.array([150,200,255])

    def processInformation(self, inimg):
        inimg = inimg.getCvBGR()
        frame = cv2.cvtColor(inimg,cv2.COLOR_BGR2HSV)
        filtered_frame = cv2.inRange(frame,self.hsv_low, self.hsv_high)
        frame_width = filtered_frame.shape[1]
        frame_height = filtered_frame.shape[0]
        contours, _ = cv2.findContours(filtered_frame, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
        filtered_contours = []
        avx,avy = 0,0
        for contour in contours:
            area = cv2.contourArea(contour)
            if (area > 10):
                filtered_contours.append(contour)
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                avx += box[:, 0].sum()/4
                avy += box[:, 1].sum()/4
                cv2.drawContours(filtered_frame, [box], 0, (227, 5, 216), 4)

        if len(filtered_contours)>0:      
            avx = int(avx/len(filtered_contours))
            avy = int(avy/len(filtered_contours))
            center_coordinates = (avx, avy)
            radius = 10
            color = (255, 0, 0)
            thickness = 2
            
            filtered_frame = cv2.circle(filtered_frame, center_coordinates, radius, color, thickness)
        else:
            avx,avy = 320/2,240/2

        # cv2.putText(filtered_frame, "JeVois RapidReact", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))         
        # cv2.putText(filtered_frame, (3, frame_height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        sendData = str((avx-frame_width/2)*60/frame_width)+";"+str(avy)
        # sendData = "10.1;3200"
        jevois.sendSerial(sendData)
        return filtered_frame

    def process(self, inframe, outframe):
        outframe.sendCv(self.processInformation(inframe))
        inframe.done()
    def processNoUSB(self, inframe):
        self.processInformation(inframe)
        inframe.done()