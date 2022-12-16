import cv2
import numpy as np

# TODO : read image
img = cv2.imread('img_3.png')

# TODO : convert to gray
imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# TODO : get threshold
ret, thrash = cv2.threshold(imgGry, 240, 255, cv2.CHAIN_APPROX_NONE)

# TODO : blur image
dst = cv2.GaussianBlur(img, (3, 3), 3, 0)

# TODO : canny image
edges = cv2.Canny(dst, 25, 100)

# TODO : dilate image
kernel = np.ones((10, 10), 'uint8')
img_dilation = cv2.dilate(edges, kernel, iterations=1)

# TODO : get contour and hierarchy
contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# TODO : reach hierarchy array
hierarchy = hierarchy[0]

# TODO : go around contour
for cnt in range(len(contours)):

    # TODO : parameters
    # contour area
    peri = cv2.arcLength(contours[cnt], True)
    approx = cv2.approxPolyDP(contours[cnt], 0.043 * peri, True)
    # coordinates to print
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    # font color
    color = (0, 0, 255)

    # TODO : line or carve ?
    if hierarchy[cnt][2] == -1 and hierarchy[cnt][3] == -1:
        if len(approx) == 2:
            cv2.putText(img, "line", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)
        else:
            cv2.putText(img, "carve", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)

    # TODO : author shapes but not face
    elif hierarchy[cnt][2] != -1 and hierarchy[cnt][3] == -1 and hierarchy[hierarchy[cnt][2]][2] == -1:
        if len(approx) == 3:
            cv2.putText(img, "Tringel", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)
        elif len(approx) == 4:
            # Distinguish the square from the rectangle
            x1, y1, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w) / h
            if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                cv2.putText(img, "Square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)

            else:
                x1, y1, w, h = cv2.boundingRect(approx)
                cv2.putText(img, "rectangel", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)

        else:
            cv2.putText(img, "circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)

    # TODO : is a face
    elif ((hierarchy[cnt][3] == -1) and (hierarchy[cnt][2] != -1)):
        cv2.putText(img, "face", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)

    # TODO : to print only in outer
    elif ((hierarchy[hierarchy[cnt][3]][3] == -1) and (hierarchy[cnt][2] != -1)):
        cv2.putText(img, " ", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)

    elif hierarchy[cnt][3] != -1 and hierarchy[cnt][0] == -1 and hierarchy[cnt][1] == -1:
        cv2.putText(img, " ", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)

    # TODO : fore face part
    else:
        if hierarchy[cnt][1] == -1:
            cv2.putText(img, "mouth", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)
        elif (hierarchy[hierarchy[cnt][1]][1]== -1):
            cv2.putText(img, "nose", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)
        else:
            cv2.putText(img, "eye", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, color)

# TODO : show image
cv2.imshow('shapes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
