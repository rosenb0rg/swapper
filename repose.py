"""
add notes here
"""

import numpy as np
import os
from glob import glob
from skimage.io import imread
from skimage.transform import rescale, resize
import argparse
from PRNet.api import PRN
from PRNet.utils.align_vertices import align
from PRNet.utils.write import write_obj
from char_dir import Character


def main(character):

    # ---- init PRN
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # GPU number, -1 for CPU
    prn = PRN(is_dlib=True)

    # ------------- load data
    # source images: D:\source\raupach\judgeC\raupach_judgeC_001
    # vertices: D:\characters\judgeC\vertices\judgeC_t00t
    # saving to: D:\characters\judgeC\src\align\raupach_judgeC_s001_t00t\obj

    image_folder = character.srcdir
    vertices_dir = character.vertdir
    save_folder = character.align_obj_dir

    print('\nImages from: ', image_folder)
    print('\nVertices from: ', vertices_dir)
    print('\nSaving to: ', save_folder, '\n\n')

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    types = ('*.jpg', '*.png')
    image_path_list = []

    # make a sorted list off all the source images
    for files in types:
        image_path_list.extend(glob(os.path.join(image_folder, files)))
    # total_num = len(image_path_list)
    image_path_list = sorted(image_path_list)

    # make a sorted list off all the reference vertices
    types = ('*.npy', '*.jpg')
    vert_path_list = []
    for files in types:
        vert_path_list.extend(glob(os.path.join(vertices_dir, files)))
    # total_num_vert = len(vert_path_list)
    vert_path_list = sorted(vert_path_list)

    print(vert_path_list)

    # iterate over the source images and repose with corresponding vertices
    for i, image_path in enumerate(image_path_list):
        name = image_path.strip().split('\\')[-1][:-4]

        print("\n%s\nALIGNED WITH\n%s\n" % (image_path_list[i], vert_path_list[i]))

        # read image
        image = imread(image_path)
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
        if pos is None:
            continue

        vertices = prn.get_vertices(pos)
        # takes the nth file in the directory of the vertices to "frontalize" the source image.
        can_vert = vert_path_list[i]
        save_vertices = align(vertices, can_vert)
        save_vertices[:, 1] = h - 1 - save_vertices[:, 1]

        colors = prn.get_colors(image, vertices)

        write_obj(os.path.join(save_folder, name + '.obj'), save_vertices, colors, prn.triangles)  # save 3d face(can open with meshlab)


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
