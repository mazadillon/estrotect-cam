import cv2
import numpy as np
import datetime

# Initially based on code by Abid Rahman K

cam = cv2.VideoCapture(0)
s, img = cam.read()
mod_img = img
old_cx = old_cy = 0

ORANGE_MIN = np.array([170, 100, 100],np.uint8)
ORANGE_MAX = np.array([180, 255, 255],np.uint8)

winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
cv2.namedWindow('thresh', cv2.CV_WINDOW_AUTOSIZE)

while s:
	cv2.imshow( winName,img )
	cv2.imshow('thresh',mod_img)
	s, img = cam.read()
	mod_img = img
	mod_img = cv2.blur(mod_img,(25,30))
	mod_img = cv2.cvtColor(mod_img,cv2.COLOR_BGR2HSV)
	mod_img = cv2.inRange(mod_img, ORANGE_MIN, ORANGE_MAX)
	contours,hierarchy = cv2.findContours(mod_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		moments = cv2.moments(cnt)                          # Calculate moments
		if moments['m00']!=0:
			cx = int(moments['m10']/moments['m00'])         # cx = M10/M00
			cy = int(moments['m01']/moments['m00'])         # cy = M01/M00
			moment_area = moments['m00']                    # Contour area from moment
			contour_area = cv2.contourArea(cnt)             # Contour area using in_built function
			diff_x = old_cx - cx							# Calculate movement from last saved image
			diff_x = diff_x * diff_x / 2					# Square and squareroot to avoid negatives
			diff_y = old_cy - cy
			diff_y = diff_y * diff_y / 2
			if contour_area > 5000:							# Only draw large contours
				cv2.drawContours(img,[cnt],0,(0,255,0),1)   # draw contours in green color
				cv2.circle(img,(cx,cy),5,(0,0,255),-1)		# Draw circle in centre of area
				if (diff_x > 1000 or diff_y > 1000):		# If this is a significantly different image
					cv2.imwrite("out" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".jpg",img) # Save it in a timestamped file.
					old_cx = cx
					old_cy = cy
	key = cv2.waitKey(10)
	if key == 27:
		cv2.destroyWindow(winName)
		cv2.destroyWindow('thresh')
		break

print "Goodbye"
