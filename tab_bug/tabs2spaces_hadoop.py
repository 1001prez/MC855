# -*- coding: utf-8 -*-
"""
    Launch: 
        python tabs2spaces_hadoop.py [DIR] [OPTIONS]

    Description: 
        Goes through all files in directory and sub-directories and find those who are idented with 
        tabs in place of spaces (only valid files).
        
        Non valid files are: images, compressed files and Makefiles

    DIR:
        Directory we are going to walk through (the current directory by default).

    OPTIONS:
        -c
            count files with tab idents 
            (default)
        -n
            name files with tabs that are beeing looked at 
            (if set alone is as set with c)
        -x
            change tabs for 4 spaces as identation
        -t
            prints a list of the types of files in the directory with tab identation 
            (if set alone is as set with c)
        --[file extention]
            select only one file type to be used. ex: --java|--css|--py|--js ...
            (only the first will be considered)
"""

import os
import sys

FILES_TO_TOUCH = [".java",".js", ".txt", ".xml", ".css", ".html", ".xsl", ".h", ".tex", ".py", ".c", ".json"]

def list_types(types):
    """
    """
    print "File types:"
    for f_t in types:
        print "\t{}".format(f_t)

def print_file_name(index, path, line):
    """
    """
    print "{}) {} - line {}".format(index, path, line)

def execute(file_, path):
    """
    """
    lines = []
    for l in file_:
        if "\t" in l:
            """ counting number of tabs to input in this line (tabs or 4x spaces)"""
            tabs = 0
            spaces = 0
            stop_identation = False
            char_i = 0
            while not stop_identation and char_i<len(l):
                if l[char_i] == ' ':
                    spaces +=1
                    if spaces == 4:
                        tabs +=1
                        spaces = 0
                elif l[char_i] == "\t":
                    tabs+=1
                else:
                    stop_identation = True
                char_i+=1

            """ create a string with spaces in place of tabs (for Python: 4 spaces = 1 tab) """
            spaces = ""
            for i in xrange(tabs):
                spaces += "    "

            l = l.split()
            l = spaces + " ".join(l)
            lines.append("{}\n".format(l))
        else:
            lines.append("{}\n".format(l))

    write_in_file(lines, path)

def tabs2spaces(dir_path, params, ext_filter):
    """
    """
    # count_all_files = 0
    file_types = []
    file_count = 0
    files_to_touch = (FILES_TO_TOUCH if ext_filter is None or ext_filter not in FILES_TO_TOUCH else ext_filter)
# options' flags
    print_count_bool = True
    print_file_types_bool = (True if 't' in params else False)
    print_file_names_bool = (True if 'n' in params else False)
    execute_bool = (True if 'x' in params else False)   

    
    if execute_bool and len(params) == 1:
        show_count = False

    for root, dirs, files in os.walk(dir_path, topdown=False):

        for name in files:
            file_ = os.path.join(root, name)
            file_path, file_ext = os.path.splitext(file_)
            if file_ext == "":
                file_ext = file_path.split("/")
                file_ext = file_ext[len(file_ext)-1]

            if file_ext in files_to_touch:

                if file_ext not in file_types:
                    file_types.append(file_ext)

                with open(file_, "r") as f:
                    has_tabs = False
                    count_line = 0

                    f = f.read().split("\n")
                    for l in f:                    
                        count_line += 1
                        if "\t" in l: # TODO if tab until first alphanum
                            file_count+=1
                            has_tabs = True
                            if print_file_names_bool:
                                print_file_name(file_count,os.path.join(root, name),count_line)
                            break 

                    if execute_bool and has_tabs:
                        execute(f,os.path.join(root, name))

                    # count_all_files+=1

    if print_file_types_bool and len(file_types) > 0:
        list_types(file_types)

    if print_count_bool:
        print "Total of files with tab identation: {}".format(file_count)

    # print "Total of researched files: {}".format(count_all_files)

def write_in_file(lines, path):
    """
    """
    with open(path, "w") as f:
        for l in lines:
            f.write(l)

def manageArguments():
    """
        Method that gets all parameters and file names
        - returns a list with all file paths and a list with all the parameters
    """
    dir_path = None
    param_list = []
    ext_filter = None
    sys.argv.remove(sys.argv[0])
    for arg in sys.argv:
        if arg[0] == '-':
            if arg[1] == '-' and ext_filter is None:
                ext_filter = ".{}".format(arg[2:])
            elif arg[1] != '-':
                arg = arg[1:]
                for p in arg:
                    param_list.append(p)
        elif os.path.isdir(arg):
            dir_path = arg

    return dir_path, param_list, ext_filter

def main():
    """
        main to tabs2spaces_hadoop
    """
    dir_path, param_list, ext_filter = manageArguments()

    if len(param_list) == 0:
        param_list.append('c')

    if dir_path is None:
        dir_path = os.getcwd()

    tabs2spaces(dir_path,param_list,ext_filter)


if __name__ == "__main__":
    main()