#!/usr/bin/python

"""
Used to  convert a simple python script into a python class.
It is of no use if the python script contains class declarations.
"""

import sys, os, re

PYTHON_INDENT = '\t'
PYTHON_NEW_LINE = '\n'
RELATIVE_PATH = 'class/'
# If before a method the self (self.method()) 
# is not placed, probably you have to add the
# character that exists before the method() in
# this list
valid_tokens = [
               ' ',
               '[',
               '(',
               '\t',
               '+'
               ]

def create_class_name(filename):
    filename_arr = []
    for x in filename:
        filename_arr.append(x)
    filename_arr[0] = filename[0].upper()
    new_filename_arr = []
    if not '_' in filename_arr:
        filename_arr[0] = filename[0].upper()
        new_filename_arr = filename_arr
    while '_' in filename_arr:
        i = filename_arr.index('_')
        new_filename_arr = list()
        for x in range(i):
            new_filename_arr.append(filename_arr[x])
        first = True
        for _ in range(len(filename[i:]) - 1):
            x = i + 1
            if first:
                first = False
                filename_arr[x] = filename_arr[x].upper()
            filename_arr[i] = filename_arr[x]
            new_filename_arr.append(filename_arr[x])
            i += 1
    filename = ''.join(new_filename_arr)
    filename = filename[:-3]
    return filename

def create_new_definition(definition):
    # Convert string to mutable object
    def_arr = []
    index = definition.find('(')
    if definition[index+1] == ')':
        noparams = True
    else:
        noparams = False
    i = 0
    for i in range(index):
        def_arr.append(definition[i])
    i += 1
    def_arr.append(definition[i])
    if noparams:
        self_str = 'self'
    else:
        self_str = 'self, '
    for c in self_str:
        def_arr.append(c)
    for index in definition[i+1:]:
        def_arr.append(index)
    definition_str = ''.join(def_arr)
    return definition_str

def get_method_name(line):
    i1 = line.find('def ')
    if i1 == -1: return ;
    i1 += 4
    i2 = line.find('(')
    return line[i1:i2+1] #The ( is added to the method name

def indent_and_add_self(pyfile, path): 
    inp = open(pyfile, 'r')
    new_file_name = pyfile[:-3] + "_class_tmp.py"
    out = open(path + new_file_name, 'w')
    
    after_imports = False
    end_class = False
    method_names = []
    lines = inp.readlines()
    # Indent lines and add self to method definitions
    for line in lines:
        if not after_imports:
            if 'def ' in line:
                after_imports = True
                print "[+] File: " + pyfile
                class_name = create_class_name(pyfile)
                print "\t[+] New class: " + class_name
                out.write('class ' + class_name + ':' + PYTHON_NEW_LINE)
                method_names.append(get_method_name(line))
                new_def = create_new_definition(line)
                out.write(PYTHON_INDENT + new_def)
            else:
                out.write(line)
        else:
            if 'def ' in line:
                new_def = create_new_definition(line)
                method_names.append(get_method_name(line))
                out.write(PYTHON_INDENT + new_def)
            else:
                # Special cases: end of script
                if 'if __name__' in line:
                    end_class = True
                    out.write(line)
                else:
                    if not end_class:
                        out.write(PYTHON_INDENT + line)
                    else:
                        out.write(line)
    if inp:
        inp.close()
    if out:
        out.close()
    return method_names

def add_self_to_methods(pyfile, method_names, path):
    inp = open(path + pyfile[:-3] + "_class_tmp.py", 'r')
    out = open(path + pyfile[:-3] + "_class.py", 'w')
    end_class = False
    for line in inp.readlines():
        if 'if __name__' in line: end_class = True;
        if not end_class:
            for method in method_names:
                if (method in line) and not ('def ' in line):
                    tmp_line = line.replace(method, 'self.' + method)
                    index = tmp_line.find('self.')
                    ch = tmp_line[index-1]
                    # The self. is in the middle of a token.
                    # if it is not any of this characters, 
                    # there are methods with coincident name.
                    # Perhaps, I forget valid tokens.
                    if ch in valid_tokens:
                        line = tmp_line
        out.write(line)
    if inp:
        inp.close()
    if out:
        out.close()

def remove_tmp_files(path):
    pattern = "_class_tmp.py$"
    for f in os.listdir(path):
        if re.search(pattern, f):
            os.remove(os.path.join(path, f))


def test():
    filename = "mini_qa.py"
    definition = 'def func(lol, yeah):'
    definition2 = 'def func():'
    print definition + ' --> ' + create_new_definition(definition)
    print definition2 + ' --> ' + create_new_definition(definition2)
    print filename + ' --> ' + create_class_name(filename)
    print "Method name --> " + get_method_name(definition2)
    exit(0)

if __name__ == '__main__':

    #test()

    if len(sys.argv) < 2:
        print "Usage: %s <script_file>" % (sys.argv[0])
    for pyfile in sys.argv[1:]:
        try:
            path = ''
            try:
                if not os.path.exists(RELATIVE_PATH):
                    os.makedirs(RELATIVE_PATH)
                path = RELATIVE_PATH
            except OSError, err:
                print "[+] Error creating output directory: " + str(err)
                path = './'
            # Indent and add self to method definitions
            method_names = indent_and_add_self(pyfile, path)
            # Replace each method execution with the self.method()
            add_self_to_methods(pyfile, method_names, path)
            # Remove temporal files
            remove_tmp_files(path)
        except IOError, err:
            print "Error dealing with file: %s" % str(err)

