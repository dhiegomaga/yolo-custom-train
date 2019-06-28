from __future__ import division
import numpy as np
import cv2
import glob
import random
import sys
import os

# DEFINE FOLDER WITH ALL IMAGES
folder = "result3/"
output_folder = 'result4/'

img_paths = glob.glob(folder+"*.jpg")
txt_paths = glob.glob(folder+"*.txt")
print("Will process "+str(len(img_paths))+ " images.")

img_paths.sort()
txt_paths.sort()

flag_noise = True
flag_duplicate = False
flag_flip = False
flag_translate = False

scale = 1.2
trans_x = 15
trans_y = -16

M = np.float32([[1,0,trans_x],[0,1,trans_y]])

count = 0


if(len(img_paths) != len(txt_paths)):
    print('Error with files, not same length')

for i in range(len(txt_paths)):
    stri = "Processing image " + str(count)
    print(stri)
    count+=1

    base_name = (txt_paths[i].split('/')[-1]).split('.')[0]
    img_old = cv2.imread(img_paths[i])
    img_new = np.copy(img_old)

    rows,cols,channels = img_old.shape
    col_off = 1
    row_off = 1

    f_new = None
    suffix = ''

    if flag_duplicate:
        suffix = '_dup'
        # Do nothing with the image
    
    if flag_flip:
        suffix = '_flip'

        # Flip image
        img_new = cv2.flip(img_new, 1)

    if flag_noise:
        suffix = '_noise'

        # Add random noise to image
        mean = 0
        var = 10
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(rows,cols,channels))
        gauss = gauss.reshape(rows,cols,channels)
        img_new = img_new + gauss

    if flag_translate:
        suffix = '_trans'

        # Translate image
        img_new = cv2.warpAffine(img_new, M, (cols,rows))

        # Scale image
        img_new = cv2.resize(img_new,None,fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)

        # Crop 
        nrows, ncols, channels = img_new.shape
        row_off = (nrows - rows)//2
        col_off = (ncols - cols)//2
        img_new = img_new[row_off:row_off+rows,col_off:col_off+cols, :]
    
    f = open(txt_paths[i], 'r')
    f_old = open(output_folder+base_name+'.txt', 'w')          # Original file, will be duplicated
    f_new = open(output_folder+base_name+suffix+'.txt', 'w')   # New file, modified version

    old_text = ''
    new_text = ''

    # Read each line from the text file
    for line in f:
        line = line.strip()
        old_text+=line+'\n'

        if flag_duplicate:
            new_text += line+'\n'
    
        if flag_flip:

            # Calculate new coordinates
            class_num, dx, dy, cx, cy = line.split(' ')
            dx = float(dx)
            dx = 1.0 - dx
            new_text += class_num +' '+ str(dx)+' '+ dy+' '+ cx+' '+ cy+'\n'

        if flag_noise:
            new_text += line+'\n'

        if flag_translate:

            # Calculate new coordinates
            class_num, dx, dy, cx, cy = line.split(' ')
            cx = float(cx)
            cy = float(cy)
            dx = float(dx)
            dy = float(dy)
            cx *= scale
            cy *= scale

            dxp = dx * cols
            dyp = dy * rows

            dxp = (dxp + trans_x) * scale - col_off
            dyp = (dyp + trans_y) * scale - row_off

            dx = dxp/cols
            dy = dyp/rows

            if dx < -0.1 or dx > 1.1 or dy < -0.1 or dy > 1.1:
                strs = "x: %f, y: %f" % (dx, dy)
                print(strs)

            else:
                new_text += class_num +' '+ str(dx)+' '+ str(dy)+' '+ str(cx)+' '+ str(cy)+'\n'

    f_old.write(old_text)
    f_old.close()

    f_new.write(new_text)
    f_new.close()

    cv2.imwrite(output_folder+base_name+'.jpg', img_old)
    cv2.imwrite(output_folder+base_name+suffix+'.jpg', img_new)










