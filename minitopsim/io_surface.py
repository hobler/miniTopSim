import numpy as np
import os
import re

import minitopsim.surface as su

np.set_printoptions(threshold=np.inf)


def read_surface(srf_fobj,n=1):
    filesrf = open(os.path.join("work/Aufgabe3_plot", srf_fobj), "r")
    content=filesrf.readlines()
    "c=filesrf.read()"
    x=np.zeros([])
    y=np.zeros([])
    time=0
    """for lines in content:
        if "surface" not in lines:
            x=np.append(x,float(lines.split(" ")[0]))
            y=np.append(y,float(lines.split(" ")[1].replace("\n", "")))
        elif "surface" in lines:
            c2+=1
            if(c2==n+1):
                time=float(float(lines.split(" ")[1]))
                print("time in ns:",time)
                break
    filesrf.close()"""
    count=0
    for lines in content:
        if "surface" not in lines and (count % n) == 1 :

            x=np.append(x,float(lines.split(" ")[0]))
            y=np.append(y,float(lines.split(" ")[1].replace("\n", "")))
        elif "surface" in lines:
            count += 1
            "time=float(float(lines.split(" ")[1]))"
            """print("time in ns:",time)"""
            pass

    filesrf.close()
    srf_obj=su.Surface(x,y)
    return srf_obj,time