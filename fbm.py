import os
import argparse
import re
import yaml

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
    ID_URL = 'url'
    ID_COPYTEXT = 'copy-text'

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

    def open_match(self, pattern):
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
                        with open(os.path.join(node.directory, FBMList.DIR_NAME, fbm)) as data_yaml:
                            data = yaml.safe_load(data_yaml.read())
                            if data[FBMList.ID_COPYTEXT]:
                                os.system(f'printf \%s "{data[FBMList.ID_COPYTEXT]}" | pbcopy')
                            os.system('open ' + data[FBMList.ID_URL])
                        return
        print(f'no match found :(')

def new_fbm(path, name, url, copy_text):
    path = os.path.join(path, FBMList.DIR_NAME)
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(os.path.join(path, name), 'w') as fbm:
        fbm.write(yaml.dump({
            FBMList.ID_URL: url,
            FBMList.ID_COPYTEXT: copy_text
        }))

def main(args):
    fbms = FBMList()
    if args.name:
        fbms.open_match(args.name)
        return
    if args.list:
        fbms.print()
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('name', nargs='?', default=None)
    mode.add_argument('-l', '--list', action='store_true', dest='list', help='list fbms in directory tree')
    mode.add_argument('-n', '--new', dest='new', nargs='+', metavar=('name url', 'copy-text'), type=str,
                      help=f'create new fbm in closest {FBMList.DIR_NAME} directory')
    mode.add_argument('-ni', '--new-in', dest='new_in', nargs='+', metavar=('directory name url', 'copy-text'), type=str,
                      help=f'create new fbm in matching {FBMList.DIR_NAME} directory')
    mode.add_argument('-nh', '--new-here', dest='new_here', nargs='+', metavar=('name url', 'copy-text'), type=str,
                      help=f'create new fbm in current directory')

    main(parser.parse_args())
