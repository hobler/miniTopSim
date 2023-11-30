import minitopsim.surface as su
import numpy as np
import re
import os

np.set_printoptions(threshold=np.inf)
clist1=[]
def read_surface(srf_fobj):

    filesrf = open(os.path.join("work/Aufgabe3_plot", "trench.srf"), "r")
    content=filesrf.readlines()
    x=np.zeros([])
    y=np.zeros([])

    for lines in content:
        if "surface" not in lines:
            x=np.append(x,float(lines.split(" ")[0]))
            y=np.append(y,float(lines.split(" ")[1].replace("\n", "")))
    print(y)
    "timereg = re.findall(r'(surface:\s+)(\d+.\d+)', content)"
    "print(float(timereg.group(2)))"
    "print(timereg)"
    # Each pair of parentheses is a group,\s+ is for all whitespaces, \d+ for all digits after whitespaces, point and 2nd \d+ is for the decimal places
    "tiltreg = re.search(r'(tilt=\s+)(\d+.\d+)', content)"
    # Similar to above
    "yieldreg = re.search(r'(Backscattered\s+\|\s+\d+.\d+\s+\|\s+)(\d+.\d+)', content)"
    # Get only numbers in second column which is group 2 and immediatly typcast them to float values and write them to dict with tilt as key
    "tydict[float(tiltreg.group(2))] = float(yieldreg.group(2))"
    filesrf.close()

    # Sort dictionary by key(tilt)

    srf_fobj.x=x
    srf_fobj.y=y
    return srf_fobj