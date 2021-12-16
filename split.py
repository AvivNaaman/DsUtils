import os
from shutil import copy2
from pathlib import Path
from random import shuffle

from main import is_image

SRC_FOLDER = r'D:\CaptainEye\PPE\OLD\DS_VESTS_MERGED'
DEST_FOLDER = r'D:\CaptainEye\PPE\final\ds'

# split 10-20-70 -> test-valid-train. do 1/2/7
TRAIN_RATIO = 9
VALID_RATIO = 1
TEST_RATIO = 0

if __name__ == '__main__':
    total = TRAIN_RATIO + VALID_RATIO + TEST_RATIO
    destinations = []
    destinations.extend([Path(DEST_FOLDER) / 'train'] * TRAIN_RATIO)
    destinations.extend([Path(DEST_FOLDER) / 'val'] * VALID_RATIO)
    destinations.extend([Path(DEST_FOLDER) / 'test'] * TEST_RATIO)
    for d in destinations:
        (d / 'images').mkdir(parents=True, exist_ok=True)
        (d / 'labels').mkdir(parents=True, exist_ok=True)
    flist = [f for f in os.listdir(SRC_FOLDER) if is_image(f)]
    shuffle(flist)
    for i, img_file in enumerate(flist):
        name, _ = os.path.splitext(img_file)
        ann_file = name + '.txt'
        ann_abs_path = os.path.join(SRC_FOLDER, ann_file)
        if os.path.isfile(ann_abs_path):  # image & annotation - both exist.
            # copy annotation to destination/extend
            copy2(ann_abs_path, str(destinations[i % total] / 'labels'))
            copy2(os.path.join(SRC_FOLDER, img_file), str(destinations[i % total] / 'images'))
