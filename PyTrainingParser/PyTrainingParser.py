
import sys
import argparse
### File example:
#55.444039;A;332484;0.011001587;0;1.0410156
#55.463987;9;-43;0;19;332504
#55.485353;9;-51;0;34;332524
#55.505386;9;-42;0;12;332544
#55.506044;U3;332529;1619;{"10":{"d":1.6103516,"dt":-65344.0,"snr":2,"dPow":37}}



from datetime import datetime
import os
import random
import time

import pandas
import csv
import json
import numpy as np

import matplotlib.pyplot as plt

import FrameBuilder

gArgs = []

####################
# handle arguments passed to the script
def handle_main_arg():

    global gArgs
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose", help="enable verbosity mode ", action="store_true")
    parser.add_argument("-f","--file", required=True, help="File name to read the data from")
    parser.add_argument("-o","--output", help="File name for output result")
    parser.add_argument("-a","--anchor", help="anchorid to get")
    parser.add_argument("-g","--graph", help="plot graph", action="store_true")
    gArgs = parser.parse_args()


####################
def main():
    global gArgs

    print ("Python version:"+sys.version)

    if gArgs.file:
        fb = FrameBuilder.FrameBuilder(gArgs.file, gArgs.anchor)

        if gArgs.graph:
            df= fb.getDataFrame()
            version = fb.getVersion()
            df.plot(x='Timestamp', y='Distance')
            df.plot(x='Timestamp', y='OverallRxPower')
            df.plot(x='Timestamp', y='FirstPathPower')
            if version=="U3.2":
                df.plot(x='Timestamp', y='MaxPathPower')
                df.plot(x='Timestamp', y='MaxPathVsEdgeIndex')
            else:
                df.plot(x='Timestamp', y='FirstPathIndex')
            plt.show()

        if gArgs.output:
            fb.exportToCsv(gArgs.output)
            

    print ("Script Terminated")

####################
if __name__ == "__main__":
    handle_main_arg()
    main()
