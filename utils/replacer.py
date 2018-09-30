

# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
from collections import OrderedDict
import json
import os
from os import walk
import glob
from utils.utils import rect_to_bb, shape_to_np, rotate_image, rotate
from char_dir import Character
import shutil
# from mtcnn.mtcnn import MTCNN
# import face_recognition

# construct the argument parser and parse the arguments
if __name__ == '__main__':

    # construct the argument parser and parse the arguments
    parser = argparse.ArgumentParser(description='extractor!!!')

    parser.add_argument("-s", "--Sce", type=str, required=False, default='in',
        help="scene name")
    parser.add_argument("-c", "--Char", type=str, required=False, default='out',
        help="character name")
    parser.add_argument("-S", "--Src", type=str, required=False, default='in',
        help="source number")
    parser.add_argument("-t", "--Targ", type=str, required=False, default='out',
        help="target number")
    args = parser.parse_args()
     
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    #detector = dlib.get_frontal_face_detector()


    # path for the shape predictor
    #predictor = dlib.shape_predictor("C:/local/src/feature_extractor/shape_predictor_68_face_landmarks.dat")

    #input and output directories

    character = args.Char
    scene = args.Sce    
    source = args.Src
    target = args.Targ

    character = Character(character, scene, source, target)


def main(character):
	mouth_dir = character.align_conv_dir
	out_dir = character.align_comped_dir
	alignemnts_dir = character.align_crop_dir

	print("\nmouths:", mouth_dir, "\nsave to:", out_dir, "\nalignments:", alignemnts_dir)

	if os.path.exists(out_dir):
		shutil.rmtree(out_dir, ignore_errors=True)
		os.makedirs(out_dir)

	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	#load alignments file
	with open("%s\\alignments.json" % alignemnts_dir) as handle:
	    info_dict = json.loads(handle.read())


	# print (mouth_path_list)

	mouth_path_list = []

	# for key in info_dict:
	# 	mouth_path_list.append(key)

	for file in glob.glob('%s/*.png' % mouth_dir):
		mouth_path_list.append(file)
	for file in glob.glob('%s/*.jpg' % mouth_dir):
		mouth_path_list.append(file)

	#print ('ping', mouth_path_list)

	# walk the list if cropped mouth images, detect images
	for i, mouth_path in enumerate(mouth_path_list):
		mouth_path_base = os.path.basename(mouth_path)

		#print ('%s/%s' % (face_dir, os.path.basename(mouth_path)))

		coords = info_dict[(mouth_path_base)][0]
		degrees = info_dict[(mouth_path_base)][1]
		face_path = info_dict[(mouth_path_base)][2]
		x,y,h,w = coords

		mouth_img = cv2.imread(mouth_path)
		face_img = cv2.imread(face_path)

		#rotate face image to
		face_img = rotate_image(face_img, degrees)

		#resize the added mouth to fit back into it's slot
		mouth_img = cv2.resize(mouth_img, (w, h), interpolation = cv2.INTER_CUBIC)

		#replace the corresponding region of the big image with the small image
		face_img[y:y+mouth_img.shape[0], x:x+mouth_img.shape[1]] = mouth_img
		face_img = rotate_image(face_img, -1 * degrees)

		out_file = str('%s/%s' % (out_dir,os.path.basename(mouth_path)))
		out_file = os.path.abspath(out_file)

		print (mouth_path, '\nis being composited and put here\n', out_file, '\n')

		cv2.imwrite(out_file, face_img)
