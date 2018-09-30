import argparse
from char_dir import Character
from subprocess import call, Popen, check_call
import time
import os
import glob


def main(character):
    basename = character.full_name
    obj_dir = character.align_obj_dir

    # clear out any existing  PNG files
    png_list = []
    for file in glob.glob(os.path.join(obj_dir, "*.png")):
        png_list.append(str(file))

    if len(png_list) > 0:
        for file in png_list:
            os.remove(file)
    else:
        pass

    # set some shortcuts
    mesh_open = 'C:/Program Files/VCG/MeshLab/meshlab.exe'
    kill_macro = './meshlab/killbash.exe'
    mesh_macro = './meshlab/meshlab.exe'
    mesh_kill = 'taskkill /IM meshlab.exe'

    # open meshlab to get it running, then close it again
    Popen(mesh_open)
    time.sleep(3)
    Popen(mesh_kill)
    # Popen(kill_macro)

    # create a sorted list of the obj files to work over
    obj_list = []
    for file in glob.glob(os.path.join(obj_dir, "*.obj")):
        obj_list.append(str(file))

    # for each obj file run the meshlab macro to output a png
    for i, file in enumerate(obj_list):
        copy2clip(str(basename + '_%s' % str(i).zfill(4)))
        Popen(mesh_open + ' %s' % file)
        time.sleep(.25)
        call(mesh_macro)
        call(mesh_kill)

    # make a list of all the new PNG files
    png_list = []
    for file in glob.glob(os.path.join(obj_dir, "*.png")):
        png_list.append(str(file))

    # rename all the PNGs so they're consistant
    for i, file in enumerate(png_list):
        new_file = '_'.join(file.split('_')[0:-1])
        new_file = new_file + '_' + str(i).zfill(3) + '.png'
        os.rename(file, new_file)


def copy2clip(txt):
    """
    function to put some text on the clipboard
    """
    cmd = 'echo ' + txt.strip() + '|clip'
    return check_call(cmd, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="meshlab PNG export automator")
    parser.add_argument('--character', '-c', type=str, nargs='?', help='character name')
    parser.add_argument('--scene', '-s', type=str, nargs='?', help='scene name')
    parser.add_argument('--source', '-S', type=str, nargs='?', help='source number')
    parser.add_argument('--target', '-t', type=str, nargs='?', help='target number')
    args = parser.parse_args()
    character = Character(args.character, args.scene, args.source, args.target)
    main(character)
