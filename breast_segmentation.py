import cv2
import numpy as np


# ------------------------------------
#   Breast Region Segmentation
# ------------------------------------

def breast_display(img):
    """ Respresent breast part """
    # hist = get_histogram_max_value(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    # Contour breast part
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Add the area of each contour result into contour_area_list
    contour_area_list = [len(contours)]
    count = 0
    for i in contours:
        area = cv2.contourArea(i)
        contour_area_list.append(area)
        # print "contour index ", count, " area = ", area
        count += 1

    # Get max area and draw contour on it.
    max_area_index = contour_area_list.index(max(contour_area_list)) - 1
    # cv2.drawContours(img, contours, max_area_index, (255, 0, 0), 3)

    # print "Number of contour detected ->", len(contours)
    # print "Size of max contour = ", max(contour_area_list)
    # print "Index of max region = ", max_area_index

    # Making mask to extract image to new image
    cnt = contours[max_area_index]
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [cnt], 0, 255, -1)

    res = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imwrite("result.png", res)
    return res, max(contour_area_list)


def glandular_tissue_display(img, t):
    """ Respresent glandular part """
    # hist = get_histogram_max_value(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    ret, thresh = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)

    # Contour glandular part
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Add the area of each contour result into contour_area_list
    contour_area_list = [len(contours)]

    count = 0
    for i in contours:
        area = cv2.contourArea(i)
        contour_area_list.append(area)
        # print "contour index ", count, " area = ", area
        count += 1

    # # Get max area and draw contour on it.
    # max_area_index = contour_area_list.index(max(contour_area_list)) - 1
    # cv2.drawContours(img, contours, max_area_index, (255, 0, 0), 3)
    # cv2.drawContours(img, contours, -1, (255, 0, 0), 3)  # for testing

    print "Number of contour detected ->", len(contours)
    print "Size of max contour = ", max(contour_area_list)
    # print "Index of max region = ", max_area_index

    # # Making mask to extract image to new image
    # cnt = contours[6]
    # mask = np.zeros(gray.shape, np.uint8)
    # cv2.drawContours(mask, [cnt], 0, 255, -1)
    #
    # res = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imwrite("result.png", res)

    return thresh, sum(contour_area_list)


def get_histogram_max_value(img):
    hist, bins = np.histogram(img.flatten(), 256, [0, 255])
    return hist


def image_histogram(img):
    hist = get_histogram_max_value(img)
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()
    return cdf_normalized


def otsu_threshold_value(img):
    # find normalized_histogram, and its cumulative distribution function
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_norm = hist.ravel() / hist.max()  # give hist.max = 1
    Q = hist_norm.cumsum()  # Return the cumulative sum of the elements along the given axis.

    bins = np.arange(256)  # Create set of number 0-255
    fn_min = np.inf

    thresh = -1
    all_pixel = np.sum(hist)

    for i in xrange(1, 256):

        p1, p2 = np.hsplit(hist_norm, [i])  # probabilities # p1 = amount of pixel in background

        q1 = Q[i]
        q2 = Q[255] - Q[i]  # cum sum of classes
        b1, b2 = np.hsplit(bins, [i])  # weights

        if q2 > 0:

            # finding weight
            w1 = q1 / all_pixel
            w2 = q2 / all_pixel

            # finding means
            m1 = np.sum(p1 * b1) / w1
            m2 = np.sum(p2 * b2) / w2

            # finding variances
            v1 = np.sum(((b1 - m1) ** 2) * p1) / w1
            v2 = np.sum(((b2 - m2) ** 2) * p2) / w1

            # calculates the minimization function
            # fn = (v1 * w1) + (v2 * w2)
            fn = v1 * q1 + v2 * q2
            # print fn

            if fn < fn_min:
                fn_min = fn
                thresh = i

    return thresh
