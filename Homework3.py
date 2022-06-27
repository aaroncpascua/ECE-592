import cv2 as cv
from cv2 import resize
from cv2 import COLOR_BGR2BGRA
import cvzone
import numpy as np
from os.path import exists
import matplotlib.pyplot as plt

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

    #Check if file exists
    fileExists = exists(filename)
    if not fileExists:
        print("File does not exist")
        return -1

    #Read image
    image = cv.imread(filename)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    plt.imshow(hsv)
    plt.show()

    lower_red = np.array([0,140,100])
    upper_red = np.array([180,260,245])

    red_mask = cv.inRange(hsv, lower_red, upper_red)
    cv.imshow('red mask', red_mask)

    binary_image = cv.threshold(red_mask, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
    
    kernel = np.ones((3,3), np.int8)

    opening = cv.morphologyEx(binary_image, cv.MORPH_OPEN, kernel, iterations=1)
    cv.imshow("opening", opening)
    # se = cv.getStructuringElement(cv.MORPH_RECT, (8,8))
    # bg=cv.morphologyEx(image, cv.MORPH_DILATE, se)
    # out_gray=cv.divide(image, bg, scale=255)
    # out_binary=cv.threshold(out_gray, 0, 255, cv.THRESH_OTSU )[1]

    # #cv.imshow("open image", open_image)
    # cv.imshow('out gray', out_gray)
    # cv.imshow('out binary', out_binary)

    #Blur using n * n kernel
    #blurred_image = cv.blur(brighter_image, (26,26))

    cv.waitKey(0)
    cv.destroyAllWindows()

#detectstopsignc('Stop2.JPG')
detectcircles('ColorBlobs.JPG')