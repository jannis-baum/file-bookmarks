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

class FBMError(Exception):
    pass
class NoMatchFound(FBMError):
    message = 'no match found'
class PatternEmpty(FBMError):
    message = 'given pattern is empty'
class NoNodes(FBMError):
    message = 'no fbms found in directory tree'
class IncorrectNArgs(FBMError):
    def __init__(self, function, nargs):
        self.message = f'{function} requires {nargs} {"argument" if nargs == 1 else "arguments"}.'

class FBMManager:
    DIR_NAME = '.fbms'
    ID_URL = 'url'
    ID_COPYTEXT = 'copy-text'

    def __init__(self):
        self.nodes = []
        self.__build_list(os.getcwd(), 0)

    def __build_list(self, directory, depth):
        if directory == '/Users': return
        fbms_dir = os.path.join(directory, FBMManager.DIR_NAME)
        if os.path.isdir(fbms_dir):
            self.nodes.append(FBMNode(depth, directory, os.listdir(fbms_dir)))
        self.__build_list(os.path.dirname(directory), depth + 1)

    def __assert_non_empty(self):
        if len(self.nodes) == 0: raise NoNodes
    
    @staticmethod
    def __assert_pattern_non_empty(pattern):
        if pattern == '': raise PatternEmpty

    @staticmethod
    def __open_fbm(directory, name):
        with open(os.path.join(directory, FBMManager.DIR_NAME, name)) as data_yaml:
            data = yaml.safe_load(data_yaml.read())
            if data[FBMManager.ID_COPYTEXT]:
                os.system(f'printf \%s "{data[FBMManager.ID_COPYTEXT]}" | pbcopy')
            os.system('open ' + data[FBMManager.ID_URL])

    @staticmethod
    def __create_fbm(directory, name, url, copy_text):
        path = os.path.join(directory, FBMManager.DIR_NAME)
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(os.path.join(path, name), 'w') as fbm:
            fbm.write(yaml.dump({
                FBMManager.ID_URL: url,
                FBMManager.ID_COPYTEXT: copy_text
            }))

    def list_to_print(self):
        self.__assert_non_empty()
        return '\n\n'.join([fbm.string() for fbm in self.nodes])

    def open_matching_fbm(self, pattern):
        nodes = self.nodes
        if '/' in pattern:
            pattern = pattern.split('/')
            pattern_dir = pattern.pop(0)
            FBMManager.__assert_pattern_non_empty(pattern_dir)
            nodes = [fbm for fbm in nodes if re.match(pattern_dir, os.path.basename(fbm.directory))]
            pattern = ''.join(pattern)
        FBMManager.__assert_pattern_non_empty(pattern)
        for node in nodes:
            for fbm in node.fbms:
                if re.match(pattern, fbm):
                    FBMManager.__open_fbm(node.directory, fbm)
                    return
        raise NoMatchFound
    
    def new_in_closest_dir(self, name, url, copy_text):
        self.__assert_non_empty()
        FBMManager.__create_fbm(self.nodes[0].directory, name, url, copy_text)

    def new_in_matching_dir(self, pattern_dir, name, url, copy_text):
        FBMManager.__assert_pattern_non_empty(pattern_dir)
        for node in self.nodes:
            if re.match(pattern_dir, os.path.basename(node.directory)):
                FBMManager.__create_fbm(node.directory, name, url, copy_text)
                return
        raise NoMatchFound

    def new_in_cwd(self, name, url, copy_text):
        FBMManager.__create_fbm(os.getcwd(), name, url, copy_text)

class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                        description='wip: add description')
        mode = self.parser.add_mutually_exclusive_group()
        mode.add_argument('name', nargs='?', default=None)
        mode.add_argument('-l', '--list', action='store_true', dest='list', help='list fbms in directory tree')
        mode.add_argument('-n', '--new', dest='new', nargs='+', metavar=('name url', 'copy-text'), type=str,
                        help=f'create new fbm in closest {FBMManager.DIR_NAME} directory')
        mode.add_argument('-ni', '--new-in', dest='new_in', nargs='+', metavar=('directory name url', 'copy-text'), type=str,
                        help=f'create new fbm in matching {FBMManager.DIR_NAME} directory')
        mode.add_argument('-nh', '--new-here', dest='new_here', nargs='+', metavar=('name url', 'copy-text'), type=str,
                        help=f'create new fbm in current directory')
        # wip: delete fbms
        
        self.fbmm = FBMManager()
        self.__run()

    def __run(self):
        args = self.parser.parse_args()
        try:
            if args.name:
                self.fbmm.open_matching_fbm(args.name)
            if args.list:
                print(self.fbmm.list_to_print())
            if args.new:
                if len(args.new) == 2:   self.fbmm.new_in_closest_dir(args.new[0], args.new[1], None)
                elif len(args.new) == 3: self.fbmm.new_in_closest_dir(args.new[0], args.new[1], args.new[2])
                else: raise IncorrectNArgs('-n/-new', '2 or 3')
            if args.new_in:
                print(args.new_in)
                if len(args.new_in) == 3:   self.fbmm.new_in_matching_dir(args.new_in[0], args.new_in[1], args.new_in[2], None)
                elif len(args.new_in) == 4: self.fbmm.new_in_matching_dir(args.new_in[0], args.new_in[1], args.new_in[2], args.new_in[3])
                else: raise IncorrectNArgs('-ni/-new-in', '3 or 4')
            if args.new_here:
                if len(args.new_here) == 2:   self.fbmm.new_in_cwd(args.new_here[0], args.new_here[1], None)
                elif len(args.new_here) == 3: self.fbmm.new_in_cwd(args.new_here[0], args.new_here[1], args.new_here[2])
                else: raise IncorrectNArgs('-nh/-new-here', '2 or 3')
        except Exception as e:
            self.parser.print_usage()
            print(e.message)

if __name__ == '__main__':
    Main()
