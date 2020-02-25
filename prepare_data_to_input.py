import os
from CashTill.augmentation import make_augmentation
from CashTill.resize import resize_all
from CashTill.label import make_label_from_config
from CashTill.prepare_and_split_annotation import get_annotation, split_data
from keras_yolo3.kmeans import YOLO_Kmeans
def resize():
    path_to_read = 'CashTill/RawData/*.bmp'
    shape = (352, 288)
    path_to_save = 'CashTill/AugNewRawData_352_288/'
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)

    resize_all(shape, path_to_read, path_to_save)
def augmentation():
    path_to_read = 'CashTill/AugNewRawData_352_288/*.bmp'
    make_augmentation(path_to_read)

def label():
    path_to_read = 'CashTill/AugNewRawData_352_288/*.bmp'
    class_path = "keras_yolo3/model_data/classes.txt"
    config = 'CashTill/config_file_label.json'
    if not os.path.exists('CashTill/LabelledData'):
        os.mkdir('CashTill/LabelledData')
    make_label_from_config(path_to_read, class_path, config)

def annotation_and_split():
    path_to_bmp = "CashTill/AugNewRawData_352_288/*"
    path_to_txt = 'CashTill/LabelledData/*'
    annotation = 'CashTill/AnnotationData/'
    if not os.path.exists(annotation):
        os.mkdir(annotation)
    print(path_to_bmp)
    get_annotation(path_to_bmp, path_to_txt, annotation)
    train_path = "CashTill/AnnotationData/Train/"
    test_path = "CashTill/AnnotationData/Test/"
    annotation_path = "CashTill/AnnotationData/annotation.txt"
    if not os.path.exists(train_path):
        os.mkdir(train_path)
    if not os.path.exists(test_path):
        os.mkdir(test_path)
    split_data(train_path, test_path, annotation_path)


def get_anchors():
    cluster_number = 9
    filename_train = 'CashTill/AnnotationData/Train/train.txt'
    filename_ancho = 'keras_yolo3/model_data/yolo_anchors.txt'
    kmeans = YOLO_Kmeans(cluster_number, filename_train)
    kmeans.txt2clusters()
    kmeans.save_to_file(filename_ancho)

def make_all():
    resize()
    augmentation()
    label()
    annotation_and_split()
    get_anchors()

if __name__ == '__main__':
    make_all()