import cv2 as cv
from cv2 import resize
from cv2 import COLOR_BGR2BGRA
from cv2 import DescriptorMatcher
from cv2 import RETR_EXTERNAL
from cv2 import CHAIN_APPROX_NONE
import cvzone
import numpy as np
from os.path import exists
import matplotlib.pyplot as plt
import math

def detectcircles(filename:str):
    """
    Detect the colored circles on patio brick in ColorBlobs.jpg
    Draw the detected circles on the image
    Draw a polygon conneting their centers
    """

    # Check if file exists
    fileExists = exists(filename)
    if not fileExists:
        print("File does not exist")
        return -1

    # Read image
    image = cv.imread(filename)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # Create upper and lower limits for the colors I want to find
    lower_blue = np.array([30,60,180])
    upper_blue = np.array([130,255,255])
    lower_red = np.array([160,70,140])
    upper_red = np.array([170,130,255])
    lower_green = np.array([29,60,170])
    upper_green = np.array([40,100,260])
    lower_orange = np.array([10,85,200])
    upper_orange = np.array([20,120,255])

    # Mask each color
    red_mask = cv.inRange(hsv, lower_red, upper_red)
    blue_mask = cv.inRange(hsv, lower_blue, upper_blue)
    green_mask = cv.inRange(hsv, lower_green, upper_green)
    orange_mask = cv.inRange(hsv, lower_orange, upper_orange)

    # Combine all the masks, increase contrast, and increase brightness for dumb bot to find circles
    combined_image = cv.addWeighted(red_mask, 0.5, blue_mask, 0.5, 0)
    brighter_image = cv.convertScaleAbs(combined_image, alpha=2.0, beta=100)
    combined_image = cv.addWeighted(combined_image, 0.5, green_mask, 0.5, 0)
    brighter_image = cv.convertScaleAbs(combined_image, alpha=2.0, beta=100)
    combined_image = cv.addWeighted(combined_image, 0.5, orange_mask, 0.5, 0)
    brighter_image = cv.convertScaleAbs(combined_image, alpha=2.0, beta=100)

    # Blur using n * n kernel
    blurred_image = cv.blur(brighter_image, (26,26))

    # Apply Hough tranform on the blurred image
    detected_circles = cv.HoughCircles(blurred_image, cv.HOUGH_GRADIENT, 1, 200, param1=25, param2=20, minRadius=50, maxRadius=90)

    # Draw circles that are detected
    if detected_circles is not None:

        # Convert circle parameters a, b, and r to integers
        detected_circles = np.uint16(np.around(detected_circles))

        coord = []
        for pt in detected_circles[0, :]:
            tempCoord = []
            a, b, r = pt[0], pt[1], pt[2]
            tempCoord.append(a)
            tempCoord.append(b)
            coord.append(tempCoord)

            # Draw the circumfrence of the circle
            cv.circle(image, (a,b), r, (0,255,0), 2)

            # Draw a small circle of (of radius 1) to show the center
            cv.circle(image, (a,b), 1, (0,0,255), 3)

    coords = np.array([coord],np.int32)
    final_image = cv.polylines(image, [coords], isClosed=True, color=(0,0,0), thickness=2)

    # Resize logo to 56 x 45, show final image
    logo = cv.imread('opencvlogo.PNG', cv.IMREAD_UNCHANGED)
    resized_logo = cv.resize(logo, (56,45), interpolation = cv.INTER_AREA)
    final_image = cvzone.overlayPNG(final_image, resized_logo)
    cv.imshow("Detected Circles", final_image)

    k = cv.waitKey(0)
    if k == ord('s'):
        filename = input("Enter the filename to save: ")
        cv.imwrite(filename, final_image)
    cv.destroyAllWindows()

def detectstopsign(filename:str):
    """
    Detect stop signs and put red square around found stop sign.
    Red square shows length of stop sign in pixels
    """

    # Check if file exists
    fileExists = exists(filename)
    if not fileExists:
        print("File does not exist")
        return -1

    # Read image, grayscale, Otsu's threshold
    image = cv.imread(filename)

    # Blur
    image_blur = cv.GaussianBlur(image, (7,7), 1)

    # Gray out image
    image_gray = cv.cvtColor(image_blur, cv.COLOR_BGR2GRAY)

    # Use canny edge detection
    image_canny = cv.Canny(image_gray, 150, 400)
    
    # Dilate canny
    kernel = np.ones((1,1))
    image_dilation = cv.dilate(image_canny, kernel, iterations=1)

    # Find contours, store locations of contour corners, create box around contour
    contours, hierarchy = cv.findContours(image_dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contoursimage = image_dilation.copy()
    contourTotalList = []
    for c in contours:
        contourList = []
        approx = cv.approxPolyDP(c, 0.04*cv.arcLength(c, True), True)
        area = cv.contourArea(c)
        if area > 100 and len(approx) == 8:
            cv.drawContours(contoursimage, c, -1, (255,0,255), 7)

            n = approx.ravel()
            i = 0
            for j in n:
                contourLocations =[]
                if(i%2==0):
                    x = n[i]
                    y = n[i + 1]
                    contourLocations.append(x)
                    contourLocations.append(y)
                    contourList.append(contourLocations)
                i += 1
            contourTotalList.append(np.array(contourList))

            (x, y, w, h) = cv.boundingRect(c)
            contourList.append(contourLocations)
            cv.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
            pixelLengthText = "{0} px".format(int(w*(math.sqrt(2) -1)))
            cv.putText(image, pixelLengthText, (x,y), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, 2)

    # Apply mask to isolate red
    lower_red = np.array([0,5,95])
    upper_red = np.array([90,80,245])
    red_mask = cv.inRange(image, lower_red, upper_red)

    # If the first try failed, try the same method, but using only red mask layer
    if len(contourTotalList) == 0:
        result = cv.morphologyEx(red_mask, cv.MORPH_OPEN, np.ones((2,2),np.uint8), iterations=1)
        image_blur = cv.GaussianBlur(result, (7,7), 1)
        image_canny = cv.Canny(image_blur, 150, 400)
        kernel = np.ones((2,2))
        image_dilation = cv.dilate(image_canny, kernel, iterations=1)
        contours, hierarchy = cv.findContours(image_dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        for c in contours:
            contourList = []
            approx = cv.approxPolyDP(c, 0.04*cv.arcLength(c, True), True)
            area = cv.contourArea(c)
            if area > 100 and len(approx) == 8:
                n = approx.ravel()
                i = 0
                for j in n:
                    contourLocations =[]
                    if(i%2==0):
                        x = n[i]
                        y = n[i + 1]
                        contourLocations.append(x)
                        contourLocations.append(y)
                        contourList.append(contourLocations)
                    i += 1
                contourTotalList.append(np.array(contourList))

                (x, y, w, h) = cv.boundingRect(c)
                contourList.append(contourLocations)
                cv.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
                pixelLengthText = "{0} px".format(int(w*(math.sqrt(2) -1)))
                cv.putText(image, pixelLengthText, (x,y), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, 2)

    # Use found contour locations to remove any blobs outside of stop sign
    stencil = np.zeros(red_mask.shape).astype(red_mask.dtype)
    color = [255, 255, 255]
    cv.fillPoly(stencil, contourTotalList, color) 
    result = cv.bitwise_and(red_mask, stencil)
    cv.imshow('image', image)
    cv.imshow('result', result)

    cv.waitKey()
    cv.destroyAllWindows()