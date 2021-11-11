import os
import argparse
import re

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
        self.nodes = []
        self.build_list(os.getcwd(), 0)

    def build_list(self, path, depth):
        if path == '/Users': return
        fbms_dir = os.path.join(path, FBMList.DIR_NAME)
        if os.path.isdir(fbms_dir):
            self.nodes.append(FBMNode(depth, path, os.listdir(fbms_dir)))
        self.build_list(os.path.dirname(path), depth + 1)

    def print(self):
        print('\n\n'.join([fbm.string() for fbm in self.nodes]))

    def find_match(self, pattern):
        nodes = self.nodes
        if '/' in pattern:
            pattern = pattern.split('/')
            pattern_dir = pattern.pop(0)
            pattern = ''.join(pattern)
            if pattern_dir != '':
                nodes = [fbm for fbm in nodes if re.match(pattern_dir, os.path.basename(fbm.directory))]
        if pattern != '':
            for node in nodes:
                for fbm in node.fbms:
                    if re.match(pattern, fbm):
                        os.system(f'{node.directory}/{FBMList.DIR_NAME}/{fbm}')
                        return
        print(f'no match found :(')

def main(args):
    fbms = FBMList()
    if args.name:
        fbms.find_match(args.name)
        return
    if args.list:
        fbms.print()
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', default=None)
    parser.add_argument('-l', '--list', action='store_true', dest='list', help='list fbms in directory tree')
    main(parser.parse_args())
