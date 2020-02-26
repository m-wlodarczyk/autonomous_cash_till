import cv2
import numpy as np
import glob
import json

def make_label_from_config(path_to_read="AugNewRawData_288_352/*.bmp", class_path="keras_yolo3/model_data/classes.txt", config='config_file_label.json'):
    with open(config) as json_file:
        config = json.load(json_file)

    classes_txt = open(class_path, "w+")
    for key in list(config.keys()):
        classes_txt.write("%s\n" % key)
    classes_txt.close()

    files = glob.glob(path_to_read)
    for file in files:
        if 'gummy' in file:
            class_name = 'gummy'
        elif 'peanuts' in file:
            class_name = 'peanuts'
        elif 'snickers' in file:
            class_name ='snickers'
        elif 'toffifee' in file:
            class_name = 'toffifee'
        elif 'knoppers' in file:
            class_name = 'knoppers'
        elif 'chocolate' in file:
            class_name = 'chocolate'
        elif 'cookies' in file:
            class_name = 'cookies'
        elif 'corn_cakes' in file:
            class_name = 'corn_cakes'
        elif 'bubble_gum' in file:
            class_name = 'bubble_gum'
        elif 'lollipop' in file:
            class_name = 'lollipop'
        elif 'chips' in file:
            class_name = 'chips'


        image = cv2.imread(file)  # import original image
        name = file.split("\\")[1]
        name = name.split(".")[0]

        kernel = np.ones((20, 20), np.uint8)  # creating kernel

        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert image into grayscale

        # binary image
        _, thresh = \
            cv2.threshold(src=grayscale_image, thresh=config[class_name]['thresh'], maxval=255, type=cv2.THRESH_BINARY)

        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  # performing morphological transformation - closing

        # finding contours on processed image

        (contours, _) = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        sorted_contours = sorted(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(sorted_contours[-1])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.imshow('Image',image)

        with open(f"CashTill/LabelledData/{name}.txt", "w") as f:
            f.write(
                str(x) + ", " + str(y) + ", " + str(x + w) + ", " + str(y + h) + ", " + str(config[class_name]['id']))
    
<<<<<<< HEAD


def test_label():
    paths = [
        "..\\CashTill\\AugNewRawData_352_288\\gummy_102_5.bmp",
        "..\\CashTill\\AugNewRawData_352_288\\lollipop_41.bmp",
        "..\\CashTill\\AugNewRawData_352_288\\bubble_gum_24_1.bmp",
        "..\\CashTill\\AugNewRawData_352_288\\knoppers_58_10.bmp",
        "..\\CashTill\\AugNewRawData_352_288\\chocolate_17_1.bmp",
        "..\\CashTill\\AugNewRawData_352_288\\peanuts_94_4.bmp",
        "..\\CashTill\\AugNewRawData_352_288\\corn_cakes_70_6.bmp",
        "..\\CashTill\\AugNewRawData_352_288\\chips_94_2.bmp",
        "..\\CashTill\\AugNewRawData_352_288\\snickers_66_8.bmp",
        "..\\CashTill\\AugNewRawData_352_288\\toffifee_108_2.bmp",
        "..\\CashTill\\AugNewRawData_352_288\\cookies_36_5.bmp"

    ]

    for path in paths:
        image = cv2.imread(path)  # import original image

        kernel = np.ones((20, 20), np.uint8)  # creating kernel

        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert image into grayscale

        # binary image
        _, thresh = \
            cv2.threshold(src=grayscale_image, thresh=60, maxval=255, type=cv2.THRESH_BINARY)

        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  # performing morphological transformation - closing

        # finding contours on processed image
        (contours, _) = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        sorted_contours = sorted(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(sorted_contours[-1])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        while True:
            cv2.imshow("Result", image)
            k = cv2.waitKey(30) & 0xff
            if k == ord('q'):
                cv2.destroyAllWindows()
                break

test_label()
=======

>>>>>>> f0cd3801a27af9a6dec8710c7acb1c73487cc788
