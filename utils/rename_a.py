import os
import argparse
import shutil

# os.path.join(root, dirs, files)

parser = argparse.ArgumentParser(description='renaming stuff')
parser.add_argument('-b', '--baseDir', required=True, type=str,
                        help='what directory are you in')
args = parser.parse_args()

baseDir = os.path.abspath(args.baseDir)
x = os.listdir(baseDir)
#print (x)

obj_dir = baseDir + '\\obj'
png_dir = baseDir + '\\png'
crop_dir = baseDir + '\\crop'
converted_dir = baseDir + '\\converted'
comped_dir = baseDir + '\\comped'

if not os.path.exists(obj_dir):
	os.makedirs(obj_dir)

if not os.path.exists(png_dir):
	os.makedirs(png_dir)

if not os.path.exists(crop_dir):
	os.makedirs(crop_dir)

if not os.path.exists(converted_dir):
	os.makedirs(converted_dir)

if not os.path.exists(comped_dir):
	os.makedirs(comped_dir)

print ('ping')
try:
	for root, dirs, files in os.walk(baseDir):
		for file in files:
			if file.endswith('.obj'):
				file = os.path.join(root, file)
				shutil.move(file, obj_dir)
except:
	pass

try:
	for root, dirs, files in os.walk(baseDir):
		for file in files:
			if file.endswith('.png'):
				file = os.path.join(root, file)
				shutil.move(file, png_dir)
except:
	pass

