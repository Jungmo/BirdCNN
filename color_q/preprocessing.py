# -*- coding: utf-8 -*-
import numpy as np
import cv2
import collections
#import globalvariable as gv


def cropknownroi(image, roi_x, roi_y):
    image_threshold = drop_image_quality(image, gv.numofcentroid)
    crop_image = image_threshold[roi_y:roi_y + 100, roi_x:roi_x + 100]

    return crop_image


def crop2(image):
    # TODO: use this instead of crop
    image1 = image[0:100, 0:100]
    image2 = image[100:200, 100:200]
    image3 = image[0:100, 100:200]
    image4 = image[100:200, 0:100]
    image5 = image[50:150, 50:150]
    cv2.imwrite("image1.bmp", image1)
    cv2.imwrite("image2.bmp", image2)
    cv2.imwrite("image3.bmp", image3)
    cv2.imwrite("image4.bmp", image4)
    cv2.imwrite("image5.bmp", image5)
    return image2


def crop(image):
    min = 255 * 10000
    min_x = 0
    min_y = 0
    return crop2(image), min_x, min_y

    for x in range(200 - gv.width):
        for y in range(200 - gv.width):
            crop = image[y:y + gv.width, x:x + gv.width]
            # white = sum(sum(crop))
            white = np.median(crop)
            if min > white:  # min = black
                min = white
                min_x = x
                min_y = y
    crop_image = image[min_y:min_y + gv.width, min_x:min_x + gv.width]
    return crop_image, min_x, min_y


def get_centroid(k):
    ret_centroid = []
    if k == 8:
        ret_centroid = [15, 47, 79, 111, 143, 175, 207, 239]
    elif k == 16:
        ret_centroid = [7, 23, 39, 55, 71, 87, 103, 119, 135, 151, 167, 183, 199, 215, 231, 247]
    elif k == 32:
	ret_centroid = [3 + 8*num for num in range(32)] 
    return ret_centroid


def drop_image_quality(image, k):
    centroid = []
    if k == 8:
        centroid = [15, 47, 79, 111, 143, 175, 207, 239]
    elif k == 16:
        centroid = [7, 23, 39, 55, 71, 87, 103, 119, 135, 151, 167, 183, 199, 215, 231, 247]
    elif k == 32:
	centroid = [3 + 8*num for num in range(32)] 
    x = 0
    y = 0
    dropped_image = image.copy()

    centroid_length = len(centroid)
    k = 0
    while(1):
	centroid_length = centroid_length >> 1
        k += 1
        if centroid_length == 1:
		break


    for i in dropped_image:
        for j in i:
            nearest_index = get_nearest_centroid(j, k)
            try:
		dropped_image[x][y] = centroid[nearest_index]
            except IndexError:
		print nearest_index				 
	        div = 256 >> k
	        sub = 2 << ((8-k-1)) - 1

	        ret = (j-sub) / div

	        if (j-sub)% div > sub+1:
		    ret = ret + 1
    		print j, div, sub, ret, (j-sub)%div
		exit()
	    y += 1
        x += 1
        y = 0
    return dropped_image


# TODO:O(log n)
def get_nearest_centroid(pixel, k):
    
    div = 256 >> k
    sub = 2 << ((8-k-1)) - 1

    ret = (pixel-sub) / div

    if (pixel-sub)% div > sub+1:
	ret = ret + 1
    return ret


def get_feature_for_make_model(cropped_image):
    area = [0] * gv.numofcentroid
    centroid = get_centroid(gv.numofcentroid)
    for x in range(gv.width):
        for y in range(gv.width):
            i = centroid.index(cropped_image[x][y])
            area[i] += 1
    return area


def pop_image(image):
    cv2.namedWindow("POP_IMAGE", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("POP_IMAGE", image)
    cv2.waitKey(0)
