import re
import numpy as np
import os

np.set_printoptions(threshold=np.inf)
clist1=[]


def read_surface(srf_fobj,n=1):
    c2 = 0
    filesrf = open(os.path.join("work/Aufgabe3_plot", "trench.srf"), "r")
    content=filesrf.readlines()
    x=np.zeros([])
    y=np.zeros([])
    for lines in content:
        if "surface" not in lines:
            x=np.append(x,float(lines.split(" ")[0]))
            y=np.append(y,float(lines.split(" ")[1].replace("\n", "")))
        elif "surface" in lines:
            c2+=1
            if(c2==n+1):
                time=float(float(lines.split(" ")[1]))
                print("time in ns:",time)
                break
    filesrf.close()


    srf_fobj.x=x
    srf_fobj.y=y
    return srf_fobj,time