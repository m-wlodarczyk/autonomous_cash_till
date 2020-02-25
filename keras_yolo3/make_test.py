from yolo import YOLO
from PIL import Image
import cv2
import numpy as np
from sklearn.metrics import (confusion_matrix, accuracy_score,
                             f1_score, classification_report,
                             mean_squared_error, mean_absolute_error)

def test_all_img():
    path = "../CashTill/AnnotationData/Test/test.txt"
    with open(path, "r") as f:
        lines = f.readlines()
    yolo = YOLO()
    y_true = []
    y_pred = []

    for line in lines:
        path_to_img = line.split(" ")[0]
        class_ = line.split(" ")[1].split(",")[-1]
        image = Image.open(path_to_img)
        out_classes = yolo.detect_image(image,predict=True)

        if len(out_classes)>=1:
            y_pred.append(out_classes[0])
            y_true.append(int(class_))
        else:
            y_true.append(int(class_))
            y_pred.append(-1)

    np.save("Test/y_pred_70_score_70_iou", y_pred)
    np.save("Test/y_true_70_score_70_iou", y_true)

    yolo.close_session()


def test_img():

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

    class_ = [0,9,8,4,5,1,7,10,2,3,6]
    yolo = YOLO()

    for path_to_img in paths:

        image = Image.open(path_to_img)

        r_image = yolo.detect_image(image)
        result = np.asarray(r_image)

        image = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        while True:
            cv2.imshow("Result", image)
            k = cv2.waitKey(30) & 0xff
            if k == ord('q'):
                cv2.destroyAllWindows()
                break



    yolo.close_session()


def assesment_model():

    y_pred = np.load("Test/y_pred_70_score_70_iou.npy")
    y_true = np.load("Test/y_true_70_score_70_iou.npy")

    cmatrix = confusion_matrix(y_true, y_pred)

    report = classification_report(y_true, y_pred, target_names=["not found", 'gummy', 'peanuts', 'snickers', 'toffifee', 'knoppers', 'chocolate', 'cookies', 'corn_cakes', 'bubble_gum', 'lollipop', 'chips'])
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)

    print(cmatrix)
    print(report)
    print(mse)
    print(mae)


if __name__ == '__main__':
    test_all_img()
    assesment_model()
