import re
import os

REGEX = r'\\def(\\[\w\W]+?){([\w\W]+)}'
MATCHER = re.compile(REGEX)


def edit_files(source_dir_name, result_dir_name, map):
    for root, dirs, files in os.walk(source_dir_name):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                modified_lines = get_modified_lines(f.readlines(), map)
            print os.path.join(result_dir_name, file)
            with open(os.path.join(result_dir_name, file), 'w') as f:
                f.writelines(modified_lines)


def get_modified_lines(lines, map):
    new_lines = []
    for line in lines:
        new_line = line
        for k, v in map.iteritems():
            #new_line = re.sub(r"({})(?=[^a-zA-Z])".format(k), ' \\' + v + ' ', line)
            new_line = new_line.replace(k, ' ' + v + ' ')
        new_lines.append(new_line)
    return new_lines


def gen_dict(file):
    map = dict()
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            key, value = gen_map(line)
            map[key] = value
    return map


def gen_map(line):
    return MATCHER.findall(line)[0]


if __name__ == '__main__':
    map = gen_dict('defs\\mydefs_metod.tex')
    edit_files('source', 'modified_source', map)