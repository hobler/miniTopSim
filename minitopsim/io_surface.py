"""Reading srf file

Functions:
   read_surface(srf_fobj,n): reads a srf file and returns a surface object and time

"""

import numpy as np
import os
import re

import minitopsim.surface as su

np.set_printoptions(threshold=np.inf)


#  change srf_fobj to file object
#  use npoints for reading
def read_surface(srf_fobj,n=-1):
    """Calls read_surface function to create a surface object which is then plotted

        Args:
            srf_fobj (file): the file to be plotted
            n (int): flag indicating how file should be read
        Returns:
            srf_obj (Surface): surface object
            time(float):last time of file
    """
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
    if n>=0:
        for lines in content:
            if "surface" not in lines and ((count % n) == 0):
                print(count)
                x=np.append(x,float(lines.split(" ")[0]))
                # replace not neccessary
                y=np.append(y,float(lines.split(" ")[1].replace("\n", "")))
            elif "surface" in lines:
                count += 1
                time=float(float(lines.split(" ")[1]))
                """print("time in s:",time)"""
    elif n==-1:
        for lines in content:
            if "surface" not in lines :
                x=np.append(x,float(lines.split(" ")[0]))
                y=np.append(y,float(lines.split(" ")[1].replace("\n", "")))
                if count==1:
                    break
            elif "surface" in lines:
                count+=1
                time=float(float(lines.split(" ")[1]))
                print("time in s:",time)
    elif n == -2:
        # points are reversed
        for lines in reversed(content):
            if "surface" not in lines:
                x = np.append(x, float(lines.split(" ")[0]))
                y = np.append(y, float(lines.split(" ")[1].replace("\n", "")))
            elif "surface" in lines:
                time=float(float(lines.split(" ")[1]))
                print("time in s:", time)
                break
                """print("time in s:",time)"""
    elif n <= -3:
        z=-n-3+1
        print(x)
        for lines in content:
            if "surface" not in lines:
                x = np.append(x, float(lines.split(" ")[0]))
                y = np.append(y, float(lines.split(" ")[1].replace("\n", "")))
            elif "surface" in lines:
                count += 1
                if (count == z + 1):
                    time = float(float(lines.split(" ")[1]))
                    print("time in s:", time)
                    break
    filesrf.close()
    srf_obj=su.Surface(x,y)
    return srf_obj,time