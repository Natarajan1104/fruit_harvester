# import the necessary packages
import numpy as np
import cv2

cv2.namedWindow

# load the image
image = cv2.imread("img.jpg")
min_area = 0
cx=0
cy=0


#Function to Stack any Images
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def empty(a):
	pass
def getContours(img):
    contours,hierarchy = cv2.findContours (img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area > min_area:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            

            

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)

#Trackbar to change HSV values
cv2.createTrackbar("Hue Min","TrackBars",2,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",8,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",83,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars",0,255,empty)
cv2.createTrackbar("Val Max","TrackBars",256,255,empty)
cv2.createTrackbar("Min cnt Area","TrackBars",100,400,empty)
 
while True:
    img = cv2.imread("img.jpg")
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    min_area = cv2.getTrackbarPos("Min cnt Area", "TrackBars")
    #print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgmasked = cv2.bitwise_and(img,img,mask=mask)
    
    imgContour = img.copy()
 
    imgGray = cv2.cvtColor(imgmasked,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgCanny = cv2.Canny(imgBlur,100,100)
    getContours(imgCanny)
    
    imgBlank = np.zeros_like(img)
    
    imgStack = stackImages(0.8,([img,imgGray,imgBlur],
                            [imgCanny,imgContour,imgBlank]))

    #Display Images on a frame
    imgStack = stackImages(0.8,([img,imgHSV,mask], 
                                 [imgmasked,imgGray,imgBlur],
                               [imgCanny,imgContour,imgBlank]))
    cv2.imshow("Stacked Images", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
	break

cv2.destroyAllWindows()
