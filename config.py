#!/usr/bin/env python
import sys
import os
import subprocess
import re

if __name__ == "__main__":
    p = subprocess.Popen("find .  -type f -name '*.etpl'", stdout=subprocess.PIPE,
                         shell=True)
    output, err = p.communicate()
    if len(output) == 0:
        print 'no .etpl files to deal'
        sys.exit()
    # remove the last \n
    output = output[:-1]
    file_list = output.split("\n")
    for file in file_list:
        file_handle = open(file)
        file_string = file_handle.read()
        print "[#]original str \n", file_string
        file_handle.close()
        matches = re.finditer(r"{{ _ .(\w+) (\w*)}}", file_string, re.M | re.I)
        if matches:
            for match in matches:
                env_var, default_value = match.groups()
                if not os.getenv(env_var) and default_value:
                    file_string = file_string.replace(str(match.group()), str(default_value))
                else:
                    file_string = file_string.replace(str(match.group()), str(os.getenv(env_var)))
        file_handle = open(file, 'w')
        file_handle.write(file_string)
        print "[#]edited str \n", file_string
        file_handle.close()
    for file in file_list:
        p = subprocess.Popen('''
                     for file in $(find .  -type f -name "*.etpl");do
                        mv $file ${file%.*}
                     done''', stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        print out