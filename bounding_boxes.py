from __future__ import division
import numpy as np
import cv2
import glob
import random

folder = "files/"
img_paths = glob.glob(folder+"*.jpg")
txt_paths = glob.glob(folder+"*.txt")

img_paths.sort()

txts = set()

img_width = 1
img_height = 1

saved_clicks = []
last_click = []
current_mouse = [0,0]
rectangles = []
rect_class = []

classes = []
colors = []

selected_class = 0

# Text 

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

# Mouse callback stuff
def mouse_click(event, x, y, flags, param):
    global last_click, saved_clicks, current_mouse

    if event == cv2.EVENT_MOUSEMOVE:
        current_mouse = [x,y]

    if event == cv2.EVENT_LBUTTONDOWN:
        last_click = [x, y]

    elif event == cv2.EVENT_LBUTTONUP:
        saved_clicks.append([x,y])
        last_click = []

def print_menu(c):
    global classes
    print "[Q]: exit [ESQ]: clear [ENTER]: next image"
    print "Classes:"
    for i in range(len(classes)):
        print "["+str(i)+"]"+" "+classes[i]

    print "Selected class: "+"["+str(c)+"]"+" "+classes[c]


# Get file names
for txt in txt_paths:
    txts.add(txt.split("/")[-1].split(".")[0])

# Input classes
print "Type class names [blank to finish]" 
if len(classes) == 0:
    while True:
        class_name = raw_input()
        if class_name == "" and len(classes) > 0:
            break

        if class_name != "" and class_name != "\n":
            classes.append(class_name)

# Define colors
for i in range(len(classes)):
    colors.append((random.randint(1,225), random.randint(1,225), random.randint(1,225)))

selected_class = 0
print_menu(selected_class)

# Start window
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_click)

# Get first available image 
next_image = 0
while next_image < len(img_paths):
    name = img_paths[next_image].split("/")[-1].split(".")[0]
    if(name not in txts):
        break
    next_image+=1

img = cv2.imread(img_paths[next_image])

img_width = img.shape[1]
img_height = img.shape[0]

# Main loop
while True:
    img_buff = img.copy()
    key = cv2.waitKey(1) & 0xFF

    # Add new rectangle if it has been set
    if len(saved_clicks) >=2:
        click0 = saved_clicks[0]
        click1 = saved_clicks[1]
        rectangles.append([click0[0], click0[1], click1[0], click1[1]])
        rect_class.append(selected_class)
        saved_clicks = []

    # Draw current rectangle
    if len(saved_clicks) == 1:
        pos = saved_clicks[0]
        cv2.rectangle(img_buff,(pos[0],pos[1]),(current_mouse[0],current_mouse[1]),colors[selected_class],2)

    # Draw rectangles
    for i in range(len(rectangles)):
        r = rectangles[i]
        class_i = rect_class[i]
        x1 = r[0]
        y1 = r[1]
        x2 = r[2]
        y2 = r[3]
        cv2.rectangle(img_buff,(x1,y1),(x2,y2),colors[class_i],2)

        bottomLeftCornerOfText = (x1,y1)

        cv2.putText(img_buff,classes[class_i], 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)


    # Esq
    if key == 27:
        if len(saved_clicks) == 1:
            saved_clicks = []

        else:
            rectangles = []
            rect_class = []
            last_click = []

    # Enter
    if key == 13:

        # Save things to file
        if len(rectangles) > 0 :

            img_width = img.shape[1]
            img_height = img.shape[0]
            
            filename = folder+img_paths[next_image].split("/")[-1].split(".")[0]+".txt"
            f = open(filename, "w")

            for index in range(len(rectangles)):
                r = rectangles[index]
                rclass = rect_class[index]

                x1 = r[0]
                y1 = r[1]
                x2 = r[2]
                y2 = r[3]

                x = min(x1, x2)/img_width
                width = abs(x1 - x2)/img_width
                y = min(y1, y2)/img_width
                height = abs(y1 - y2)/img_width

                line = str(rclass)+" "+str(x)+" "+str(y)+" "+str(width)+" "+str(height)+"\n"
                f.write(line)

            f.close()

        # Reset current selection
        rectangles=[]
        rect_class = []
        last_click = []

        # Next available image
        next_image+=1
        while next_image < len(img_paths):
            name = img_paths[next_image].split("/")[-1].split(".")[0]
            print name
            if(name not in txts):
                break
            next_image+=1

        img = cv2.imread(img_paths[next_image])

    if key >= ord("0") and key <= ord("9") and key-48 < len(classes):
        selected_class = key-48
        print_menu(selected_class)

    if key == ord("q"):
        break

    

    cv2.imshow('image',img_buff)