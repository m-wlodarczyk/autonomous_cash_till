import cv2
import glob

def resize_all(shape=(352, 288), path_to_read='RawData/*.bmp', path_to_save="NewRawData_288_352/"):
    files = glob.glob(path_to_read)
    for file in files:
        img = cv2.imread(file)
        img = cv2.resize(img, shape)
        name = file.split("\\")[1]
        cv2.imwrite(path_to_save+str(name), img)