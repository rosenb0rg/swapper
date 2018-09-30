import os

class Character:
    """
    a "character" class that lets you store all the location of subfiles for the conversion
    process and quickly pull specific
    """
    def __init__(self, name='', scene='', source='', target=''):
        base = 'D:\\'
        # judgeC
        self.name = name
        # raupach
        self.scene = scene
        # 003
        self.source = source
        # 03b
        self.target = target
        
        # raupach_judgeC_s003_t03b
        self.full_name = scene + "_" + name +"_s" + str(source) + "_t" + str(target)
        
        # D:/characters/judgeC/
        self.basedir = os.path.join(base, 'characters', self.name)
        
        # D:/characters/judgeC/face/
        self.facedir = os.path.join(self.basedir, 'face')
        
        # D:/characters/judgeC/src/align
        self.aligndir = os.path.join(self.basedir, 'src', 'align')
        
        # D:/characters/judgeC/src/comp
        self.compdir = os.path.join(self.basedir, 'src', 'comp')
        
        # D:/source/raupach/judgeC/raupach_judgeC_001
        self.srcdir = os.path.join(base, 'source', self.scene, self.name, self.scene + '_' + self.name + '_' + self.source )
        
        # D:/characters/judgeC/vertices/raupach_t10
        self.vertdir = os.path.join(self.basedir, 'vertices', self.name + "_t" + self.target)
        
        
        # subdirectories for align workflow elements
        # D:/characters/judgeC/src/align/<full name>/obj
        self.align_obj_dir = os.path.join(self.aligndir, self.full_name, 'obj')
        
        # D:/characters/judgeC/src/align/<full name>/obj
        self.align_png_dir = os.path.join(self.aligndir, self.full_name, 'obj')
        
        # D:/characters/judgeC/src/align/<full name>/crop
        self.align_crop_dir = os.path.join(self.aligndir, self.full_name, 'crop')
        # D:/characters/judgeC/src/align/<full name>/converted
        self.align_conv_dir = os.path.join(self.aligndir, self.full_name, 'converted')
        
        # D:/characters/judgeC/src/align/<full name>/comped_b
        self.align_comped_dir = os.path.join(self.aligndir, self.full_name, 'comped_b')

        # subdirectories for faceswap_mod process
        # D:/characters/judgeC/face/raupach_t10
        self.swap_head_dir = os.path.join(self.facedir, self.name + '_t' + str(target))
        
        # D:/characters/judgeC/comp/raupach_t10
        self.swap_comp_dir = os.path.join(self.compdir, self.full_name)


        # subdirectories for deepfakes
        # D:/characters/judgeC/df/model_GAN128
        self.model_dir = os.path.join(self.basedir, 'df', 'model_GAN128')
        
        # D:/source/00_training/crop
        self.imgA_dir = os.path.join(base, 'source', '00_training', 'crop')
        
        # D:/characters/judgeC/df/imgB
        self.imgB_dir = os.path.join(self.basedir, 'df', 'imgB_crop')
        
        # D:/characters/judgeC/df/imgB_crop
        self.imgB_crop_dir = os.path.join(self.basedir, 'df', 'imgB')

if __name__ == "__main__":
    x = Character('judgeC', 'raupach', '001', '00b')
    # print (x.swap_comp_dir)