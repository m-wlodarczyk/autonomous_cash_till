import numpy as np
import cv2
import zmq
import threading
import base64
import sys
from PIL import Image, ImageDraw, ImageFont
from yolo import YOLO
from object_position import check_object_position, check_boxs
import math
import os

products_name = [
    'gummy 1 6.49',
    'peanuts 1 4.99',
    'snickers 1 1.89',
    'toffifee 1 6.39',
    'knoppers 1 1.79',
    'chocolate 1 4.29',
    'cookies 1 5.19',
    'corn_cakes 1 3.51',
    'bubble_gum 1 0.99',
    'lollipop 1 0.99',
    'chips 1 3.49',

]

#products_name = ['gummy', 'peanuts', 'snickers', 'toffifee', 'knoppers', 'chocolate',
#                 'cookies', 'corn_cakes', 'bubble_gum', 'lollipop', 'chips']
class Video:
    def __init__(self):
        context = zmq.Context()

        self.__footage_socket = context.socket(zmq.PUB)
        self.__footage_socket.bind('tcp://127.0.0.1:5555')

        self.__msg_socket = context.socket(zmq.REP)
        self.__msg_socket.bind('tcp://127.0.0.1:8888')

        self.__msg_socket_2 = context.socket(zmq.REP)
        self.__msg_socket_2.bind('tcp://127.0.0.1:8889')

        self.__run = True
        self.yolo = YOLO()



        end_rec_thread = threading.Thread(target=self.end_recording)
        end_rec_thread.start()

        self.run()


    def send_item(self, final_products):
        for p, n in zip(final_products, products_name):
            if p == 1:
                self.__footage_socket.send_multipart([b'item', str.encode(n)])

    def play_video(self,  num):
        self.__run = True
        products = np.zeros(11)
        num_frame = 0

        vid_path =  ["D:\\Projects\\autonomic_cash_till\\keras_yolo3\\video\\11_products.mp4",
                     "D:\\Projects\\autonomic_cash_till\\keras_yolo3\\video\\pairs.mp4"]
        vid = cv2.VideoCapture(vid_path[num])


        while self.__run:
            try:
                return_value, frame = vid.read()
                image = cv2.resize(frame, (800, 600))

            except:
                print('Open Error! Try again!')
                break
            else:

                if check_object_position(image):

                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    r_image, out_boxes, out_scores, out_classes = self.yolo.detect_image(image, test=True)

                    print(out_boxes)
                    x = check_boxs(out_boxes, out_scores, out_classes)


                    print(x, out_classes, out_scores)
                    print(products)
                    try:
                        if x != -1 and x!=None:
                            products[x]+=1
                        else:
                            for id in out_classes:
                                products[id] +=1
                    except:
                        continue
                    num_frame+=1

                    result = np.asarray(r_image)

                    image = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
                    image = cv2.resize(image, (800, 600))


                else:
                    if num_frame != 0:
                        out = np.divide(products, num_frame)
                        print(out)
                        final_products = [math.ceil(i) if i > 0.1 else 0 for i in out]
                        self.send_item(final_products)
                        products = np.zeros(11)
                        num_frame = 0


                encoded, buffer = cv2.imencode('.jpg', image)
                jpg_as_text = base64.b64encode(buffer)
                self.__footage_socket.send_multipart([b"video", jpg_as_text])
            # k = cv2.waitKey(30) & 0xff
            # if k == ord('q'):
            #     cv2.destroyAllWindows()
            #     break
    def record_camera(self):
        self.__run = True
        camera = cv2.VideoCapture(0)


        products = np.zeros(11)


        i = 0
        while self.__run:
            try:
                return_value, frame = camera.read()
                image = cv2.resize(frame, (800, 600))

            except:
                print('Open Error! Try again!')
                break
            else:
                if check_object_position(image):

                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    r_image, out_boxes, out_scores, out_classes = self.yolo.detect_image(image, test=True)

                    # print(out_boxes)
                    x = check_boxs(out_boxes, out_scores, out_classes)
                    try:

                        if x != -1 and x != None:
                            products[x] += 1
                        else:
                            for id in out_classes:
                                products[id] += 1
                    except:
                        continue
                    i += 1
                    result = np.asarray(r_image)
                    image = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
                    # cv2.imshow("Result", image)
                else:
                    if i != 0:
                        out = np.divide(products, i)

                        final_products = [math.ceil(i) if i > 0.1 else 0 for i in out]
                        self.send_item(final_products)
                        products = np.zeros(11)
                        i = 0

                    # cv2.imshow("Result", image)

                encoded, buffer = cv2.imencode('.jpg', image)
                jpg_as_text = base64.b64encode(buffer)
                self.__footage_socket.send_multipart([b"video", jpg_as_text])


    def end_recording(self):
        while True:
            message = self.__msg_socket.recv_string()
            if message == "False":
                self.__run = False
                self.__msg_socket.send_string("Ending recording")

    def run(self):
        while True:
            cmd = self.__msg_socket_2.recv_string()
            if cmd == "camera":
                self.__msg_socket_2.send_string("Starting camera")
                self.record_camera()
            elif cmd == "video1":
                self.__msg_socket_2.send_string("Playing video")
                self.play_video(0)
            elif cmd == "video2":
                self.__msg_socket_2.send_string("Playing video")
                self.play_video(1)

Video()



