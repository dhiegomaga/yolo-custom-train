# yolo-custom-train
Easy-to-use tool for labeling and training yolo object detector with custom images. 

*Note¹*: This repository is based on [Yolo Object Detector](https://pjreddie.com/darknet/yolov2/). More info on training for custom images/classes can be found [here](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects). 

*Note²*: Currently only supports 10 classes, need to make some modifications to accept more, sorry. 

## Requisites

Python 2.7 with cv2. 
In order to run darknet, you'd also need OpenCV libs for C++ and CUDA for visualization and performance. 
I also only tested in Linux, but should work on Windows 

## How to use 

### Installing Yolo

You'll need it to train and test results. Donwload and follow these instructions [here](https://github.com/AlexeyAB/darknet).

### Labeling 

1. Download this repository

2. Put images inside of *files/*

3. Edit [bounding_boxes.py classes](https://github.com/dhiegomaga/yolo-custom-train/blob/master/bounding_boxes.py#L14) to match your object classes. 

4. Run `python bounding_boxes.py`

*Controls:* Press a number 0-9 to select a class, CLICK to start drawing rectangle, ESQ to clear selections, ENTER to save for current image, Q to quit. **You can close and open the program without losing progress.**

### Generating config files 

1. Edit [config_files.py classes](https://github.com/dhiegomaga/yolo-custom-train/blob/master/config_files.py#L8). They have to match the list you edited previously in bounding_boxes.py exactly!

2. Run `python config_files.py`

3. Copy a *.cfg* file from the darknet repository into the *cfg2/* folder. I recomend the **yolov2.cfg** (already included), as it is the only one that's worked reliably for me so far. 

4. Change the *.cfg* file: `batch=32`, `subdivisions=8`, `classes=<n_classes>`, `filters=(<n_classes> + 5)*5`. 

5. Move files to the *darknet/* folder: 

    `cp train.txt darknet/ &&c p test.txt darknet/ && cp -r cfg2/ darknet/ && cp -r files/ darknet/`
    
6. Download convolutional weights for training `cd darknet/; wget https://pjreddie.com/media/files/darknet19_448.conv.23`.

### Training

Inside of the darknet folder: 

`mkdir backup` <- really important

`./darknet detector train cfg2/obj.data cfg2/yolov2.cfg darknet19_448.conv.23` <- Change to your .cfg file

### Testing

First change the **yolov2.cfg** file inside yolo for testing configuration: `batch=1`, `subdivisions=1`. 

Finally: 

./darknet detector test cfg2/obj.data cfg2/yolov2.cfg backup/yolov2.weights <your-image-path>

Disclaimer: There is an 'official' tool for labeling classes, but I find it very slow to use, and it doesn't handle configuration files. You can find it [here](https://github.com/AlexeyAB/Yolo_mark). 

