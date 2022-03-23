import libjevois as jevois
import cv2
import numpy as np
import json

class Vision:
    
    def __init__(self):
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        
    def process(self, inframe, outframe):
        inimg = inframe.getCvBGR()
        frame = cv2.cvtColor(inimg,cv2.COLOR_BGR2HSV)
        hsv_low = np.array([10,100,100])
        hsv_high = np.array([150,255,255])
        filtered_frame = cv2.inRange(frame,hsv_low, hsv_high)
        
        contours, hierarchy = cv2.findContours(filtered_frame, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
        filtered_contours = []
        avx,avy = 0,0
        for contour in contours:
            area = cv2.contourArea(contour)
            if (area > 200):
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
            frame_width = filtered_frame.shape[1]

            print("Angle To Turn: ", (avx-frame_width/2)*70/frame_width)
        cv2.putText(filtered_frame, "JeVois RapidReact", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))         
        fps = self.timer.stop()
        height = filtered_frame.shape[0]
        width = filtered_frame.shape[1]
        cv2.putText(filtered_frame, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        sendData = str(avx-width/2)+";"+str(avy)
        jevois.sendSerial("usb hi there great")
        jevois.sendSerial(sendData)
        outframe.sendCv(filtered_frame)
        inframe.done()
    def processNoUSB(self, inframe):
        inimg = inframe.getCvBGR()
        frame = cv2.cvtColor(inimg,cv2.COLOR_BGR2HSV)

        hsv_low = np.array([40,100,100])
        hsv_high = np.array([80,255,255])
                
        filtered_frame = cv2.inRange(frame,hsv_low, hsv_high)
        
        contours, hierarchy = cv2.findContours(filtered_frame, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
        filtered_contours = []
        avx,avy = 0,0
        for contour in contours:
            area = cv2.contourArea(contour)
            if (area > 200):
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
            frame_width = filtered_frame.shape[1]

            print("Angle To Turn: ", (avx-frame_width/2)*70/frame_width)
        cv2.putText(filtered_frame, "JeVois RapidReact", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))         
        fps = self.timer.stop()
        height = filtered_frame.shape[0]
        width = filtered_frame.shape[1]
        cv2.putText(filtered_frame, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        sendData = str(avx-width/2)+";"+str(avy)
        jevois.sendSerial("nousb sad but oh welp")
        jevois.sendSerial(sendData)
        inframe.done()