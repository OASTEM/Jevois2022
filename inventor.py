import libjevois as jevois
import cv2
import numpy as np
import json

## Me
#
# Add some description of your module here.
#
# @author Tom Bob
# 
# @videomapping YUYV 320 240 60 YUYV 320 240 60 Me RapidReact
# @email bob@yay.com
# @address 123 first street, Los Angeles CA 90012, USA
# @copyright Copyright (C) 2018 by Tom Bob
# @mainurl stuff.com
# @supporturl stuff.com
# @otherurl stuff.com
# @license 
# @distribution Unrestricted
# @restrictions None
# @ingroup modules
class Vision:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvBGR()
        frame = cv2.cvtColor(inimg,cv2.COLOR_BGR2HSV)
        # Display the resulting frame

        # 240°, 6%, 60%
        h = 140/2
        threshold = 30
        hsv_low = np.array([h-threshold,40,100])
        hsv_high = np.array([h+threshold,200,255])

        h = 120/2
        threshold = 20
        hsv_low = np.array([100,100,100])
        hsv_high = np.array([200,255,255])
        
        
        # image_width = 640
        # image_height = 480
        # focal_length = 696.195
        # actual_width = 39
        
        # centerX = 0
        # centerY = 0
        
        filtered_frame = cv2.inRange(frame,hsv_low, hsv_high)
        
        contours, hierarchy = cv2.findContours(filtered_frame, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
        filtered_contours = []
        avx,avy = 0,0
        for contour in contours:
            area = cv2.contourArea(contour)
            if (1500 > area > 200):
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
            
            # Using cv2.circle() method
            filtered_frame = cv2.circle(filtered_frame, center_coordinates, radius, color, thickness)
            # cv2.circle(filtered_frame,(avx/len(filtered_contours),avy/len(filtered_contours)), 3, (0,255,0), -1)
            frame_width = filtered_frame.shape[1]
            # print("RPM: ", avy*25+3000)
            # print("WIDTH: ",frame_width)
            # print("center",avx)
            # print("Direction: ", avx-frame_width/2)
            # if avx-frame_width/2 > 0: print("turn right")
            # else: print("turn left")
            # if -50 < avx-frame_width/2 < 50: print("SHOOT")
            print("Angle To Turn: ", (avx-frame_width/2)*70/frame_width)
        # Write a title:
        cv2.putText(filtered_frame, "JeVois RapidReact", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
        # Write frames/s info from our timer into the edge map (NOTE: does not account for output conversion time):
        fps = self.timer.stop()
        height = filtered_frame.shape[0]
        width = filtered_frame.shape[1]
        cv2.putText(filtered_frame, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        sendData = {"x":avx-width/2,"y":avy}
        sendData = {"x":100,"y":200}
        jevois.sendSerial(json.dumps(sendData))
        # Convert our output image to video output format and send to host over USB:
        outframe.sendCv(filtered_frame)
        inframe.done()
        
