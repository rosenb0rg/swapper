These big files need to be added in the follow hierarchy for everything to work


        Data/net-data/256_256_resfcn256_weight.data-00000-of-00001
        Data/shape_predictor_68_face_landmarks.dat
        faceswap/lib/face_alignment/.cache/2DFAN-4.h5


in ./misc/environment.yaml is the info for the conda enviroment for all this to work.


Swapper has several modes.

vert

    In vert mode you provide swapper with a character's name and target shot number.

        python master.py -m vert -c judgeC -t 00

    The program looks in the character\face folder (D:\characters\judgeC\face), since the cropped faces are easier for the algorithm to detect. It looks at each frame of the specified target shot and outputs 'vertices' information to the character\vertices folder. This data files are used in the repose process.

repose
    
    In repose mode you provide swapper with a characters name, scene, source shot, and target shot. 

        python master.py -m repose -c judgeC -s raupach -S 001 -t 00

    The progam looks at each frame from the source shot for that scene, makes a 3D face object from the 2D image, and 'reposes' it to match the orientation of the target shot. The output files land in the character\src\align\shot-name\obj folder.

mesh

    In mesh mode you provide swapper with a character's name and target shot number.

        python master.py -m mesh -c judgeC -s raupach -S 001 -t 00

    This script runs a macro which opens MeshLab, adjusts some settings, and outputs a PNG of each reposed obj file. The results land in the same character\src\align\shot-name\obj folder.


