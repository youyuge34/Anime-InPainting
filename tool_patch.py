#!/usr/bin/env python
# author: youyuge34@github
"""
===============================================================================
Interactive Image Patching Tool using Edge-Connect algorithm.


USAGE:
    python tool_patch.py --path <your weights directory path>
                         --edge (optional to open edge window)


README FIRST:
    Two windows will show up, one for input and one for output.
    if `--edge` arg is input, another edge window will show up.
    [Important] Switch your typewriting into ENG first.

    At first, in input window, draw black in the missing part using
mouse left button. Then press 'n' to patch the image (once or a few times)
For any finer touch-ups, you can press any of the keys below and draw lines on
the areas you want. Then again press 'n' for updating the output.
    In input window, left mouse is to draw the black mask which means the defect.
    In edge window, left mouse is to draw the edge while right mouse is to erase the edges.
    Press '[' and ']' to resize the brush thickness, as in PhotoShop.
    Finally, press 's' to save the output.

Key '[' - To make the brush thickness smaller
Key ']' - To make the brush thickness larger
Key '0' - Todo
Key '1' - Todo

Key 'n' - To patch the black part of image, just use input image
Key 'e' - To patch the black part of image, use the input image and edit edge
Key 'r' - To reset the setup
Key 's' - To save the output
Key 'q' - To quit
===============================================================================
"""

# Python 2/3 compatibility
from __future__ import print_function

import argparse
import glob

from easygui import *
import numpy as np
import cv2 as cv
import sys
import os
import shutil
from src.config import Config
from main import main

BLUE = [255, 0, 0]  # rectangle color
RED = [0, 0, 255]  # PR BG
GREEN = [0, 255, 0]  # PR FG
BLACK = [0, 0, 0]  # sure BG
WHITE = [255, 255, 255]  # sure FG

DRAW_MASK = {'color': BLACK, 'val': 255}

radius = 3  # brush radius
drawing = False
drawing_edge_l = False
drawing_edge_r = False
value = DRAW_MASK
THICKNESS = -1  # solid brush circle 实心圆


def onmouse_input(event, x, y, flags, param):
    """
    mouse callback function, whenever mouse move or click in input window this function is called.
    只要鼠标在input窗口上移动(点击），此函数就会被回调执行
    """
    # to change the variable outside of the function
    # 为方法体外的变量赋值，声明global
    global img, img2, drawing, value, mask, ix, iy, rect_over
    # print(x,y)

    # draw touchup curves
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        cv.circle(img, (x, y), radius, value['color'], THICKNESS, lineType=cv.LINE_AA)
        cv.circle(mask, (x, y), radius, value['val'], THICKNESS, lineType=cv.LINE_AA)

    elif drawing is True and event == cv.EVENT_MOUSEMOVE:
        cv.circle(img, (x, y), radius, value['color'], THICKNESS, lineType=cv.LINE_AA)
        cv.circle(mask, (x, y), radius, value['val'], THICKNESS, lineType=cv.LINE_AA)

    elif drawing is True and event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.circle(img, (x, y), radius, value['color'], THICKNESS, lineType=cv.LINE_AA)
        cv.circle(mask, (x, y), radius, value['val'], THICKNESS, lineType=cv.LINE_AA)


def onmouse_edge(event, x, y, flags, param):
    """
    mouse callback function, whenever mouse move or click in edge window this function is called.
    只要鼠标在edge窗口上移动(点击），此函数就会被回调执行
    """
    # to change the variable outside of the function
    # 为方法体外的变量赋值，声明global
    global img, img2, drawing_edge_l, drawing_edge_r, value, mask, ix, iy, edge
    # print(x, y)

    # draw touchup curves
    if event == cv.EVENT_LBUTTONDOWN:
        drawing_edge_l = True
        # cv.circle(edge, (x, y), 1, WHITE, THICKNESS, lineType=cv.LINE_AA)
        edge[y, x] = 255

    elif drawing_edge_l is True and event == cv.EVENT_MOUSEMOVE:
        # cv.circle(edge, (x, y), 1, WHITE, THICKNESS, lineType=4)
        edge[y, x] = 255

    elif drawing_edge_l is True and event == cv.EVENT_LBUTTONUP:
        drawing_edge_l = False
        # cv.circle(edge, (x, y), 1, WHITE, THICKNESS, lineType=cv.LINE_AA)
        edge[y, x] = 255

    elif event == cv.EVENT_RBUTTONDOWN:
        drawing_edge_r = True
        cv.circle(edge, (x, y), radius, BLACK, THICKNESS, lineType=cv.LINE_AA)

    elif drawing_edge_r is True and event == cv.EVENT_MOUSEMOVE:
        cv.circle(edge, (x, y), radius, BLACK, THICKNESS, lineType=cv.LINE_AA)

    elif drawing_edge_r is True and event == cv.EVENT_RBUTTONUP:
        drawing_edge_r = False
        cv.circle(edge, (x, y), radius, BLACK, THICKNESS, lineType=cv.LINE_AA)


def check_load(args):
    """
    Check the directory and weights files. Load the config file.
    """
    if not os.path.exists(args.path):
        raise NotADirectoryError('Path <' + str(args.path) + '> does not exist!')

    edge_weight_files = list(glob.glob(os.path.join(args.path, 'EdgeModel_gen*.pth')))
    if len(edge_weight_files) == 0:
        raise FileNotFoundError('Weights file <EdgeModel_gen*.pth> cannot be found under path: ' + args.path)
    inpaint_weight_files = list(glob.glob(os.path.join(args.path, 'InpaintingModel_gen*.pth')))
    if len(inpaint_weight_files) == 0:
        raise FileNotFoundError('Weights file <InpaintingModel_gen*.pth> cannot be found under path: ' + args.path)

    config_path = os.path.join(args.path, 'config.yml')
    # copy config template if does't exist
    if not os.path.exists(config_path):
        shutil.copyfile('./config.yml.example', config_path)

    # load config file
    config = Config(config_path)

    return config


def load_model(config):
    """
    Load model, the key function to interact with backend.
    """
    model = main(mode=4, config=config)
    return model


def model_process(img, mask, edge=None):
    """
    Patch the image with mask. Key function.
    :param img: Input dimension 3
    :param mask: Mask dimension 2
    :return:
    """
    # print(img.shape, mask.shape)
    mask[mask > 0] = 255
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    if edge is None:
        result, edges = model.test_img_with_mask(img, mask)
    else:
        result, edges = model.test_img_with_mask(img, mask, edge_edit=edge)
    result = cv.cvtColor(result, cv.COLOR_RGB2BGR)
    return result, edges


if __name__ == '__main__':

    # print documentation
    print(__doc__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='path of model weights files <.pth>')
    parser.add_argument('-e', '--edge', action='store_true', help='open the edge edit window')
    args = parser.parse_args()

    # check the exist of path and the weights files
    config = check_load(args)
    model = load_model(config)

    # image: absolute image path
    image = fileopenbox(msg='Select a image', title='Select', filetypes=[['*.png', '*.jpg', '*.jpeg', 'Image Files']])
    if image is None:
        print('\nPlease select a image.')
        exit()
    else:
        print('Image selected: ' + image)

    img = cv.imread(image)

    # resize the photo if it is too small
    if max(img.shape[0], img.shape[1]) < 256:
        img = cv.resize(img, dsize=(0, 0), fx=1.5, fy=1.5, interpolation=cv.INTER_CUBIC)
    img2 = img.copy()  # a copy of original image
    mask = np.zeros(img.shape[:2], dtype=np.uint8)  # mask initialized to PR_BG
    output = np.zeros(img.shape, np.uint8)  # output image to be shown

    # input and output windows
    cv.namedWindow('output')
    cv.namedWindow('input')
    cv.setMouseCallback('input', onmouse_input)
    cv.moveWindow('input', img.shape[1] + 20, 90)  # move input window

    if args.edge:
        edge = np.zeros(img.shape, np.uint8)
        cv.namedWindow('edge')
        cv.setMouseCallback('edge', onmouse_edge)
        cv.moveWindow('edge', img.shape[1] + 40, 90)

    while 1:
        cv.imshow('output', output)
        cv.imshow('input', img)
        if args.edge:
            cv.imshow('edge', edge)
        k = cv.waitKey(200)

        # key bindings
        if k == 27 or k == ord('q'):  # esc to exit
            break
        elif k == ord('0'):  # BG drawing
            print(" mark background regions with left mouse button \n")
            value = DRAW_MASK

        # TODO: edge model
        # elif k == ord('1'):  # FG drawing
        #     print(" mark foreground regions with left mouse button \n")
        #     value = DRAW_FG

        elif k == ord('r'):  # reset everything
            print("resetting \n")
            drawing = False
            value = DRAW_MASK
            img = img2.copy()
            mask = np.zeros(img.shape[:2], dtype=np.uint8)  # mask initialized to PR_BG
            output = np.zeros(img.shape, np.uint8)  # output image to be shown
            if args.edge:
                edge = np.zeros(img.shape, np.uint8)
                drawing_edge_r = False
                drawing_edge_l = False

        elif k == ord('n'):  # begin to path the image
            print("\nPatching using input image...")
            output, edge = model_process(img, mask)
            print("\nPatched!")
        elif k == ord('e') and args.edge:  # begin to path the image
            print("\nPatching using input and edge...")
            output, _ = model_process(img, mask, edge)
            print("\nPatched!")
        elif k == ord('['):
            radius = 1 if radius == 1 else radius - 1
            print('Brush thickness is', radius)
        elif k == ord(']'):
            radius += 1
            print('Brush thickness is', radius)
        elif k == ord('s'):
            path = filesavebox('save', 'save the output.', default='patched_' + os.path.basename(image),
                               filetypes=[['*.jpg', 'jpg'], ['*.png', 'png']])
            if path:
                if not path.endswith('.jpg') and not path.endswith('.png'):
                    path = str(path) + '.png'
                cv.imwrite(path, output)
                print('Patched image is saved to', path)
    cv.destroyAllWindows()
