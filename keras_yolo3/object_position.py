import cv2
import numpy as np

def check_object_position(frame):

    thres = 50
    line_X = 400

    kernel = np.ones((20, 20), np.uint8)  # creating kernel

    grayscale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert image into grayscale

    # binary image
    _, thresh = \
        cv2.threshold(src=grayscale_image, thresh=60, maxval=255, type=cv2.THRESH_BINARY)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  # performing morphological transformation - closing

    # cv2.imshow("erosion", erosion)
    #cv2.imshow("dilate", dilation)

    # Find contours on image
    try:
        (contours, _) = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_sorted = sorted(contours, key=lambda x: cv2.contourArea(x))  # sorted contours ascending
        # (x, y, w, h) = cv2.boundingRect(contours_sorted[-1])
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        M = cv2.moments(contours_sorted[-1])
          # calculate moments (-1 because the last one has the bigger Area)
        # cx = M10/M00 cy = M01/M00dane
        X = int(M["m10"] / M["m00"])


        X_array = [X+x for x in range(-thres,thres)]

        if line_X in X_array:
            return True
        else:
            return False
    except:
        return False


def intersection_over_union(boxA, boxB):
    """
    Implementation from https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
    :param boxA:
    :param boxB:
    :return:
    """
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou

def check_boxs(out_boxes, out_scores, out_class):
    try:
        num = len(out_boxes)
        all_iou = []
        if num > 1:
            for i in range(num):
                for j in range(i + 1, num):
                    iou = intersection_over_union(out_boxes[i], out_boxes[j])
                    if iou > 0.5:
                        all_iou.append([i, j])
            for i in range(len(all_iou)):
                a, b = all_iou[i]

                if out_scores[a] > out_scores[b]:
                    return out_class[a]
                else:
                    return out_class[b]
        else:
            return -1
    except:
        return -1
