import os
import glob
import shutil

# remove every fourth frame and then rename....FUCK

file_dir = os.path.abspath('D:\\characters\\judgeC\\target_drop\\judgeC_t00')



for i in glob.glob(file_dir + '/*.png'):
	istr = str(i)
	if istr.endswith('0.png') or istr.endswith('5.png'):
		print ('removing: ', i)
		os.remove(i)

for i, file in enumerate(glob.glob(file_dir + '/*.png')):
	file_str = str(file)
	img_num = '{0:03d}'.format(i)
	renamed = file_str[:-7] + str(img_num) + '.png'
	print ('\nrenamed: ', renamed)
	shutil.move(file, renamed)