import os

SRC_FILE = r'D:\CaptainEye\PPE\final\ds\train\labels'
# mapping of classes: ({src,src,src},dest)
MAP = [
    ({3, 4, 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22}, 1)
]

if __name__ == '__main__':
    for filename in os.listdir(SRC_FILE):
        if filename.endswith('.txt'):
            # SOURCE LINES
            with open(os.path.join(SRC_FILE, filename), 'r') as f:
                lines = f.readlines()
            final_lines = []
            for l in lines:
                splitted = l.rstrip().replace('\t', ' ').split(' ')
                old_c = int(splitted[0])
                dsts = [m[1] for m in MAP if old_c in m[0]]
                if dsts:
                    splitted[0] = str(dsts[0])
                final_lines.append(' '.join(splitted))
            with open(os.path.join(SRC_FILE, filename), 'w') as f:
                for line in final_lines:
                    f.write(line + '\n')
