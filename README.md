# Autonomic Cash Till
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)
## Introduction

A Keras implementation of YOLOv3 (Tensorflow backend) inspired by [qqwweee/keras-yolo3](https://github.com/qqwweee/keras-yolo3).

## Requirements 


## Model 
1. Download from link https://1drv.ms/u/s!AkIRi7wDenNBhYxXl5W2oG7ASRyEkA?e=oTqxZi or prepare own model. 
### Prepare own model 
1. Prepare input data 
   * Add image data to folder CashTill/RawImageData. 
   * Prepare file classes.txt
   * Update files config_file_label.json and label.py 
   * Run script prepare_data_to_input.py to make:
       * resize raw image  
       * augmentation 
       * label 
       * annotation 
       * split data 
       * make anchors 
    ```
   python prepare_data_to_input.py
   ```
   * Update files config_file.json
   * Train model 
   ```
   python train.py 
   ```
## Aplication
 ![GUI](https://github.com/m-wlodarczyk/autonomic_cash_till/blob/master/electron_app/gui_1.png)
 ![GUI](https://github.com/m-wlodarczyk/autonomic_cash_till/blob/master/electron_app/gui_2.png)
 ![GUI](https://github.com/m-wlodarczyk/autonomic_cash_till/blob/master/electron_app/gui_3.png)
## Run Tensorobard 
Run command in folder keras_yolo3
 ```
   tensorboard --logdir log_dir/logs/scalars/20200107-162253
 ```
 ![Tensorboard](https://github.com/m-wlodarczyk/autonomic_cash_till/blob/master/keras_yolo3/tensorboard_scalars.png)
