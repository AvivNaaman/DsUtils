import os
from shutil import copy2


def open_classes(folder, mode='r'):
    return open(os.path.join(folder, 'classes.txt'), mode)


image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff']


def is_image(fname):
    _, extension = os.path.splitext(fname)
    return extension in image_extensions


def copy_merge_annotation(src_filepath, dest_filepath, original_classes: list, new_classes: list):
    with open(src_filepath, 'r') as src:
        src_lines = [r.rstrip() for r in src.readlines()]
    # for each line, replace class #, and write back.
    dst_lines = []
    for line in src_lines:
        line.replace('\t', ' ')
        splitted = line.split(' ')
        class_id = int(splitted[0])
        new_class_num = new_classes.index(original_classes[class_id])
        splitted[0] = str(new_class_num)
        dst_lines.append(' '.join(splitted))

    with open(dest_filepath, 'w') as dest:
        for line in dst_lines:
            dest.write(line + '\n')


if __name__ == '__main__':
    MAIN_DS_FOLDER = r'D:\CaptainEye\DS_ASHDOD'
    SECONDARY_DS_FOLDER = r'D:\CaptainEye\DS_CHV'
    TARGET_FOLDER = r'D:\CaptainEye\DS_VESTS_F'
    # Classes merging - first
    with open(os.path.join(MAIN_DS_FOLDER, 'classes.txt')) as main_classes:
        all_classes = [line.rstrip() for line in main_classes.readlines()]
    # second
    original_secondary_classes = []
    with open(os.path.join(SECONDARY_DS_FOLDER, 'classes.txt')) as secondary_classes:
        for line in secondary_classes.readlines():
            newc = line.rstrip()
            original_secondary_classes.append(newc)
            if newc not in all_classes:
                all_classes.append(newc)

    # copy all files from first to target; for each annotation file, replace the class IDs
    print("Copying 1st files")
    for filename in [f for f in os.listdir(MAIN_DS_FOLDER) if is_image(f)]:
        name, ext = os.path.splitext(filename)
        ann_abs_path = os.path.join(MAIN_DS_FOLDER, name + '.txt')
        # image has annotation. copy both to target.
        if os.path.isfile(ann_abs_path):
            copy2(os.path.join(MAIN_DS_FOLDER, filename), TARGET_FOLDER)
            copy2(ann_abs_path, TARGET_FOLDER)
        else:
            print(f"Image {filename} in 1st has no annotation file!")

    # copy files from secondary to target.
    print("Copying 2nd files")
    for filename in [f for f in os.listdir(SECONDARY_DS_FOLDER) if is_image(f)]:
        name, _ = os.path.splitext(filename)
        ann_abs_src_path = os.path.join(SECONDARY_DS_FOLDER, name + '.txt')
        ann_abs_dest_path = os.path.join(TARGET_FOLDER, name + '.txt')
        # annotation file does not exist
        if not os.path.isfile(ann_abs_src_path):
            print(f"Image {filename} in 2nd has no annotation file!")
            continue
        # no duplicates!
        while os.path.isfile(ann_abs_dest_path):
            name += '_2'
            ann_abs_dest_path = os.path.join(TARGET_FOLDER, name + '.txt')
        # finish copy of image + annotation
        copy2(os.path.join(SECONDARY_DS_FOLDER, filename), TARGET_FOLDER)
        copy_merge_annotation(ann_abs_src_path, ann_abs_dest_path, original_secondary_classes, all_classes)

    print("Writing classes.txt file")
    # write a new classes.txt file to target
    with open_classes(TARGET_FOLDER, 'w') as final_classes_file:
        for cls in all_classes:
            final_classes_file.write(cls + '\n')

    exit(0)
