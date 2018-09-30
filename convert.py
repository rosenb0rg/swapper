import os
import argparse
from char_dir import Character
import shutil
import faceswap

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='converter!!!')
	parser.add_argument("-s", "--Sce", type=str, required=False, default='in',
		help="scene name")
	parser.add_argument("-c", "--Char", type=str, required=False, default='out',
		help="character name")
	parser.add_argument("-S", "--Src", type=str, required=False, default='in',
		help="source number")
	parser.add_argument("-t", "--Targ", type=str, required=False, default='out',
		help="target number")
	args = parser.parse_args()

	scene_name = args.Sce
	character_name = args.Char
	source_number = args.Src
	target_number = args.Targ

	character = Character(character_name, scene_name, source_number, target_number)
	main(character)

def main(character):
	in_dir = character.align_crop_dir
	out_dir = character.align_conv_dir
	model_dir = character.model_dir

	if not os.path.exists(in_dir):
		os.makedirs(in_dir)

	if os.path.exists(out_dir):
		shutil.rmtree(out_dir, ignore_errors=True)
		os.makedirs(out_dir)

	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	print ('\ninput: ', in_dir, '\noutput: ', out_dir, '\nmodel: ', model_dir)

	os.system("python ./faceswap/faceswap.py convert -i %s -o %s --model-dir %s -t GAN128 -b 0" % (in_dir, out_dir, model_dir))