import argparse
from char_dir import Character
import out_vert
import repose
import mesh
import utils.extractor as extractor
import convert
import utils.replacer as replacer
import utils.faceswap_mod as fswap
import train

"""
make a module that will:
- run any mode, given character, scene, source, target, etc.

- be OS independet

- can leave the separate modules so you can run them on on image, etc.

steps are:

train: train a neural net for particular character against the source face

vert: get the vertices of the from the character's target shot

repose: get reoriented OBJ files of a source shot matched to a target shot

mesh: macro to run through meshlab and output PNGs of the reoriented source
face

crop: crop the moths of the reoriented source face

convert: convert the mouths of the source face into the mouth of the target
face, using the trained neural net

comp: place the converted mouths back onto the source face

swap: composite the frankenstein face onto the target footage. This goes into
aftereffects

"""


def main(args):
    mode = str(args.mode)
    char = str(args.character)
    scene = str(args.scene)
    source = str(args.source)
    targ = str(args.target)
    crop_mode = args.crop_mode

    if mode or char or scene or source or targ is not None:
        character = Character(char, scene, source, targ)
        runn(mode, character, crop_mode)
    else:
        welcome()


def welcome():
    mode = input('What operation?: ')
    char = input('Character: ')
    scene = input('Scene: ')
    source = input('Source: ')
    targ = input('Target: ')

    character = Character(char, scene, source, targ)

    runn(mode, character)


def runn(mode, character, crop_mode):
    if mode == 'vert':
        out_vert.main(character)

    if mode == 'repose':
        repose.main(character)

    if mode == 'mesh':
        mesh.main(character)

    if mode == 'crop':
        extractor.main(character, crop_mode)

    if mode == 'convert':
        convert.main(character)

    if mode == 'comp':
        replacer.main(character)

    if mode == 'swap':
        fswap.main(character)

    if mode == 'train':
        train.main(character)

def over_dir(function):
    pass

if __name__ == "__main__":

    help_text = """Welcome to the swapper. First pick what mode you want to use: vert will extract reference vertices given a character and a target shot. repose will create 3D oject from a source shot, and rotate to match the orientation of the target face, and save that as an obj. mesh will loop a macro to open each of these OBJ files and save a png."""

    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument('--mode', '-m', type=str, nargs='?', help='mode: repose, vertices, etc.')
    parser.add_argument('--character', '-c', type=str, nargs='?', help='character name')
    parser.add_argument('--scene', '-s', type=str, nargs='?', help='scene name')
    parser.add_argument('--source', '-S', type=str, nargs='?', help='source number')
    parser.add_argument('--target', '-t', type=str, nargs='?', help='target number')
    parser.add_argument('--crop_mode', '-C', type=str, nargs='?', help='crop mode', default=0)

    args = parser.parse_args()

    main(args)
