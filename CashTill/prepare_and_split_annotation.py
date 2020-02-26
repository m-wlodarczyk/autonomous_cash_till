import os
import glob
import random

def get_annotation(bmp="AugNewRawData_352_288/*", txt="LabelledData/*", new="CashTill/AnnotationData"):


    path_bmp = sorted(glob.glob(bmp))
    path_txt = sorted(glob.glob(txt))

    print(path_bmp)

    for bmp, txt in zip(path_bmp, path_txt):
        with open(txt, "r") as f:
            line = f.readline()
        print(bmp, txt)
        print(line.split(","))
        x_min,y_min,x_max,y_max, class_id  = line.split(",")
        x_min = int(x_min)
        y_min = int(y_min)
        x_max = int(x_max)
        y_max = int(y_max)
        class_id = int(class_id)

        with open(new+'annotation.txt', "a") as f:
            f.write("../"+bmp + " "+ str(x_min)+ ","+ str(y_min)+ ","+ str(x_max)+ ","+ str(y_max)+ ","+str(class_id)+"\n")



def split_data(train_path = "CashTill/AnnotationData/Train/", test_path = "CashTill/AnnotationData/Test/",  annotation_path = "CashTill/AnnotationData/annotation.txt"):

    with open(annotation_path, "r") as f:
        data = f.read()
    data = data.split("\n")
    test_ = random.choices(data, k=int(len(data)*0.2))
    train_ = list(set(data) - set(test_))
    with open(train_path+"train.txt", "w") as f:
        for t in train_:
            f.write(t+"\n")
    with open(test_path + "test.txt", "w") as f:
        for t in test_:
            f.write(t+"\n")


if __name__ == '__main__':
    get_annotation()
    split_data()
