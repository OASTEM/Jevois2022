# import the opencv library
import cv2
import numpy as np
  
# define a video capture object
vid = cv2.VideoCapture(0)
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # Display the resulting frame

    # 240°, 6%, 60%
    h = 120/2
    threshold = 20
    hsv_low = np.array([h-threshold,100,40])
    hsv_high = np.array([h+threshold,255,255])
    
    h = 140/2
    threshold = 30
    hsv_low = np.array([h-threshold,40,40])
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
        print("RPM: ", avy*25+3000)
        frame_width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        print("WIDTH: ",frame_width)
        print("center",avx)
        print("Direction: ", avx-frame_width/2)
        if avx-frame_width/2 > 0: print("turn right")
        else: print("turn left")
        if -50 < avx-frame_width/2 < 50: print("SHOOT")
    cv2.imshow('frame', filtered_frame)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()