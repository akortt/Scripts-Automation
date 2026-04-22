import sys
import os

if len(sys.argv) == 2:
    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print('[-] ' + filename + ' does not exist.')
        exit(0)
    elif not os.access(filename, os.R_OK): # Check if file can be read.
        print("[-] " + filename + ' access denied.')
        exit(0)

    print("(+) Reading Vulnerabilities from: " + filename)
    # If we attempt to execute the command and provide an argument, this will be placed in the sys.argv[1]
    # E.g. python introduction.py vul-banner.txt

