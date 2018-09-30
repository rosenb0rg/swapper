"""
a script to extract the orientation vertices from a 2D target image
so you can later repose another 2D image.
"""
import numpy as np
import os
from glob import glob
from skimage.transform import rescale, resize
from skimage.io import imread
import argparse
from char_dir import Character
from PRNet.api import PRN


def main(character):
    # ---- init PRN
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # GPU number, -1 for CPU
    prn = PRN(is_dlib=True)

    # ------------- load data
    # e.g. d:\characters\richardson\face\richardson_t10
    image_folder = os.path.join(character.swap_head_dir)
    print('\nImage Folder: ', image_folder)

    # e.g. d:\characters\richardson\vertices\richardson_t10
    save_folder = os.path.join(character.vertdir)
    print('\nSave Folder: ', save_folder)

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    types = ('*.jpg', '*.png')
    image_path_list = []
    for files in types:
        image_path_list.extend(glob(os.path.join(image_folder, files)))
    # total_num = len(image_path_list)
    # print (total_num)

    for i, image_path in enumerate(image_path_list):
        get_vert(image_path, save_folder, prn)


def get_vert(image_path, save_folder, prn):

    prn = prn
    image = imread(image_path)
    name = os.path.basename(image_path)
    name = name.split('.')[0]
    print(name)
    [h, w, _] = image.shape

    # the core: regress position map
    if True:
        # if args.isDlib:
        max_size = max(image.shape[0], image.shape[1])
        if max_size > 1000:
            image = rescale(image, 1000./max_size)
            image = (image*255).astype(np.uint8)
        pos = prn.process(image)  # use dlib to detect face
    else:
        if image.shape[1] == image.shape[2]:
            image = resize(image, (256, 256))
            pos = prn.net_forward(image/255.)  # input image has been cropped to 256x256
        else:
            box = np.array([0, image.shape[1]-1, 0, image.shape[0]-1])  # cropped with bounding box
            pos = prn.process(image, box)

    image = image/255.
    # if pos is None:
    #     continue

    vertices = prn.get_vertices(pos)
    np.save("%s/%s" % (save_folder, name), vertices)
    # save_vertices = vertices.copy()
    # save_vertices[:,1] = h - 1 - save_vertices[:,1]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Tom's Swapper!")

    parser.add_argument('--mode', '-m', type=str, nargs='?', help='mode: repose, vertices, etc.')
    parser.add_argument('--character', '-c', type=str, nargs='?', help='character name')
    parser.add_argument('--scene', '-s', type=str, nargs='?', help='scene name')
    parser.add_argument('--source', '-S', type=str, nargs='?', help='source number')
    parser.add_argument('--target', '-t', type=str, nargs='?', help='target number')

    args = parser.parse_args()

    character = Character(args.character, args.scene, args.source, args.target)

    main(character)
