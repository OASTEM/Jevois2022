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
        hsv_low = np.array([h-threshold,100,40])
        hsv_high = np.array([h+threshold,255,255])
        
        
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
                # adjusted for turned camera
                avx += box[:, 1].sum()/4
                avy += box[:, 0].sum()/4
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
            # print("RPM: ", avy*25+3000)
            frame_width = inimg.shape[1]
            # print("WIDTH: ",frame_width)
            # print("center",avx)
            # print("Direction: ", avx-frame_width/2)
            # if avx-frame_width/2 > 0: print("turn right")
            # else: print("turn left")
            # if -50 < avx-frame_width/2 < 50: print("SHOOT")
        # cv2.imshow('frame', filtered_frame)
            
        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()
    
        # Detect edges using the Laplacian algorithm from OpenCV:
        #
        # Replace the line below by your own code! See for example
        # - http://docs.opencv.org/trunk/d4/d13/tutorial_py_filtering.html
        # - http://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
        # - http://docs.opencv.org/trunk/d5/d0f/tutorial_py_gradients.html
        # - http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
        #
        # and so on. When they do "img = cv2.imread('name.jpg', 0)" in these tutorials, the last 0 means they want a
        # gray image, so you should use getCvGRAY() above in these cases. When they do not specify a final 0 in imread()
        # then usually they assume color and you should use getCvBGR() above.
        #
        # The simplest you could try is:
        #    outimg = inimg
        # which will make a simple copy of the input image to output.
        outimg = cv2.Laplacian(filtered_frame, -1, ksize=5, scale=0.25, delta=127)
        
        # Write a title:
        cv2.putText(outimg, "JeVois RapidReact", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
        # Write frames/s info from our timer into the edge map (NOTE: does not account for output conversion time):
        fps = self.timer.stop()
        height = outimg.shape[0]
        width = outimg.shape[1]
        cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        sendData = {"x":avx-frame_width/2,"y":avy}
        sendData = {"x":100,"y":200}
        jevois.sendSerial(json.dumps(sendData))
        # Convert our output image to video output format and send to host over USB:
        outframe.sendCv(filtered_frame)
        inframe.done()
        
