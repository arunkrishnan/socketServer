#!/usr/bin/env python
'''
   Program to run main py by assigning random port
'''

from random import randint
import subprocess
import time

if "__main__" == __name__:
    port = str(randint(8080,8085))
    fd = subprocess.Popen(['python','main.py',port])
    time.sleep(5)
    subprocess.Popen(['firefox','localhost:' + port])
    fd.close()
