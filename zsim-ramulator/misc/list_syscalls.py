#!/usr/bin/python
# Produces a list of syscalls in the current system
import os, re
unistdpath = "/usr/include/asm/unistd.h"
if os.path.exists(unistdpath) == False:
	unistdpath = "/usr/include/asm-generic/unistd.h"
	if os.path.exists(unistdpath) == False:
		raise Exception("Could not find path to unistd.h! Neither /usr/include/asm/unistd.h nor /usr/include/asm-generic/unistd.h exist!")
syscallCmd = "gcc -E -dD " + unistdpath + " | grep __NR"
syscallDefs = os.popen(syscallCmd).read()
sysList = [(int(numStr), name) for (name, numStr) in re.findall("#define __NR_(.*?) (\d+)", syscallDefs)]
denseList = ["INVALID"]*(max([num for (num, name) in sysList]) + 1)
for (num, name) in sysList: denseList[num] = name
print '"' + '",\n"'.join(denseList) + '"'
