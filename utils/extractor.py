# import numpy as np
import argparse
# import imutils
# import dlib
import cv2
# from collections import OrderedDict
import json
import glob
import os
# from math import atan2, degrees, radians
# import math
# from tqdm import tqdm
import shutil
from utils.utils import get_rot_angle, rotate_image
from char_dir import Character
from mtcnn.mtcnn import MTCNN


def main(character, mode_num=0):

    if mode_num == 0:
        in_dir = character.align_png_dir
        out_dir = character.align_crop_dir
    else:
        in_dir = character.imgB_dir
        out_dir = character.imgB_crop_dir

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir, ignore_errors=True)
        os.makedirs(out_dir)

    if not os.path.exists(in_dir):
        os.makedirs(in_dir)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # save_name = character.full_name

    print("\ninput directory:", in_dir, '\noutput directory:', out_dir)

    extensions = ['.png', '.jpg', '.jpeg']

    image_path_list = []

    for extension in extensions:
        for i, file in enumerate(glob.glob('%s/*%s' % (in_dir, extension))):
            image_path_list.append(file)

    image_path_list = sorted(image_path_list)

    # print (image_path_list)

    # create an empty dictionary for filename, coordinate info
    # to be written to a json file for the replacer script on the other side
    info_dict = {}

    # walk the list of input images, detect images
    detector = MTCNN()

    if not os.path.isfile('%s/already_cropped.json' % in_dir):
        with open('%s/already_cropped.json' % in_dir, 'w') as outfile:
            json.dump('already cropped!', outfile, indent=4)
            outfile.write("\n")

        for i, image_path in enumerate(image_path_list):
            try:
                image = cv2.imread(str(image_path))    
                results = detector.detect_faces(image)[0]
                x, y, w, h = results['box'] 

                pad = int(.3*h)
                x -= pad
                w += 2*pad
                y -= pad
                h += 2*pad

                image = image[y:y+h, x:x+w]
            
                # write over the existing image with the cropped one
                cv2.imwrite(image_path, image)

                # redetect mouth points to extract just the mouth
                mleft = detector.detect_faces(image)[0]['keypoints']['mouth_left']
                mright = detector.detect_faces(image)[0]['keypoints']['mouth_right']
                print (image_path)

                # determine degrees needed to rotate the image to be aligned
                degrees = get_rot_angle(mleft, mright)

                # rotate original image to align
                image_r = rotate_image(image, degrees)

                # detect new mouth points (could replace with math)
                mleft = detector.detect_faces(image_r)[0]['keypoints']['mouth_left']
                mright = detector.detect_faces(image_r)[0]['keypoints']['mouth_right']

                # create coordinates for bounding box
                w = mright[0] - mleft[0]
                h = w
                x = mleft[0]
                y = mleft[1] - h/2
                print (x, y, w, h)

                # add pixels of padding as a percentage of the width
                pad = int(round(.6*w))
                x -= pad
                x = int(x)
                y -= pad
                y = int(y)
                h += 2*pad
                h = int(h)
                w += 2*pad
                w = int(w)

                coords = [x, y, h, w]

                #basename for files
                filename = os.path.basename(image_path)

                # location of the cropped face and source image
                out_path = '%s/%s' % (out_dir, filename)
                in_path = '%s/%s' % (in_dir, filename)

                # add cropped output file path, coordinates and input 
                # file path to dictionary
                info_dict[filename] = coords, degrees, in_path

                # add padding and resize to 128 pixels
                roi = image_r[y:y + h, x:x + w]
                roi = cv2.resize(roi, (128, 128))
                #roi = imutils.resize(roi, 128, inter=cv2.INTER_CUBIC)

                # write image
                cv2.imwrite(out_path, roi)
            except:
                print ('whhoopppss!')
                pass

    if os.path.isfile('%s/already_cropped.json' % in_dir):
        print ('Already Cropped!')
        for i, image_path in enumerate(image_path_list):
            try:
                image = cv2.imread(str(image_path))
                # redetect mouth points to extract just the mouth
                mleft = detector.detect_faces(image)[0]['keypoints']['mouth_left']
                mright = detector.detect_faces(image)[0]['keypoints']['mouth_right']
                print (image_path)

                # determine degrees needed to rotate the image to be aligned
                degrees = get_rot_angle(mleft, mright)

                # rotate original image to align
                image_r = rotate_image(image, degrees)

                # detect new mouth points (could replace with math)
                mleft = detector.detect_faces(image_r)[0]['keypoints']['mouth_left']
                mright = detector.detect_faces(image_r)[0]['keypoints']['mouth_right']

                # create coordinates for bounding box
                w = mright[0] - mleft[0]
                h = w
                x = mleft[0]
                y = mleft[1] - h/2
                print (x, y, w, h)

                # add pixels of padding as a percentage of the width
                pad = int(round(.6*w))
                x -= pad
                x = int(x)
                y -= pad
                y = int(y)
                h += 2*pad
                h = int(h)
                w += 2*pad
                w = int(w)

                coords = [x,y,h,w]

                #basename for files
                filename = os.path.basename(image_path)

                # location of the cropped face and source image
                out_path = '%s/%s' % (out_dir, filename)
                in_path = '%s/%s' % (in_dir, filename)

                # add cropped output file path, coordinates and input
                # file path to dictionary
                info_dict[filename] = coords, degrees, in_path

                # add padding and resize to 128 pixels
                roi = image_r[y:y + h,x:x + w]
                roi = cv2.resize(roi, (128,128))
                #roi = imutils.resize(roi, 128, inter=cv2.INTER_CUBIC)

                # write image
                cv2.imwrite(out_path, roi)

            except:
                print ('oh no!')
                raise

        try:
            with open('%s/alignments.json' % out_dir, 'w') as outfile:
                json.dump(info_dict, outfile, indent=4)
                outfile.write("\n")
        except:
            pass

def process(image_path):
    '''
    eventually implement this to cleanup the code
    '''
    image = cv2.imread(str(image_path))
    # redetect mouth points to extract just the mouth
    mleft = detector.detect_faces(image)[0]['keypoints']['mouth_left']
    mright = detector.detect_faces(image)[0]['keypoints']['mouth_right']
    print (image_path)

    # determine degrees needed to rotate the image to be aligned
    degrees = get_rot_angle(mleft, mright)

    # rotate original image to align
    image_r = rotate_image(image, degrees)

    # detect new mouth points (could replace with math)
    mleft = detector.detect_faces(image_r)[0]['keypoints']['mouth_left']
    mright = detector.detect_faces(image_r)[0]['keypoints']['mouth_right']

    # create coordinates for bounding box
    w = mright[0] - mleft[0]
    h = w
    x = mleft[0]
    y = mleft[1] - h/2
    print (x, y, w, h)

    # add pixels of padding as a percentage of the width
    pad = int(round(.6*w))
    x -= pad
    x = int(x)
    y -= pad
    y = int(y)
    h += 2*pad
    h = int(h)
    w += 2*pad
    w = int(w)

    coords = [x,y,h,w]

    #basename for files
    filename = os.path.basename(image_path)

    # location of the cropped face and source image
    out_path = '%s/%s' % (out_dir, filename)
    in_path = '%s/%s' % (in_dir, filename)

    # add cropped output file path, coordinates and input
    # file path to dictionary
    info_dict[filename] = coords, degrees, in_path

    # add padding and resize to 128 pixels
    roi = image_r[y:y + h,x:x + w]
    roi = cv2.resize(roi, (128,128))
    #roi = imutils.resize(roi, 128, inter=cv2.INTER_CUBIC)

    # write image
    cv2.imwrite(out_path, roi)

if __name__ == '__main__':

    # construct the argument parser and parse the arguments
    parser = argparse.ArgumentParser(description='extractor!!!')

    parser.add_argument("-s", "--Sce", type=str, required=False, default='in', help="scene name")
    parser.add_argument("-c", "--Char", type=str, required=False, default='out', help="character name")
    parser.add_argument("-S", "--Src", type=str, required=False, default='in', help="source number")
    parser.add_argument("-t", "--Targ", type=str, required=False, default='out', help="target number")
    parser.add_argument("-m", "--Mode", type=int, required=False, default=0, help="mode 0 runs normally, mode 1 will crop faces for training given a character only")
    args = parser.parse_args()

    character = args.Char
    scene = args.Sce
    source = args.Src
    target = args.Targ
    mode_num = args.Mode

    character = Character(character, scene, source, target)

    main(character, mode_num)
