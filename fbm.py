import os
import argparse

class FBMNode:
    def __init__(self, depth, directory, fbms):
        self.depth = depth
        self.directory = directory
        self.fbms = fbms

    def string(self):
        return f'\n{" " * self.depth}├── '.join([f'{"." * self.depth}{os.path.basename(self.directory)}/'] + self.fbms[:-1]) \
             + f'\n{" " * self.depth}└── ' + self.fbms[-1]

class FBMList:
    DIR_NAME = '.fbms'

    def __init__(self):
        self.fbms = []
        self.build_list(os.getcwd(), 0)

    def build_list(self, path, depth):
        if path == '/Users': return
        fbms_dir = os.path.join(path, FBMList.DIR_NAME)
        if os.path.isdir(fbms_dir):
            self.fbms.append(FBMNode(depth, path, os.listdir(fbms_dir)))
        self.build_list(os.path.dirname(path), depth + 1)

    def print(self):
        print('\n\n'.join([fbm.string() for fbm in self.fbms]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', action='store_true', dest='list', help='list fbms in directory tree')
    args = parser.parse_args()

    fbms = FBMList()

    if args.list:
        fbms.print()
