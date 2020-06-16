
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
    gArgs = parser.parse_args()


####################
def main():
    global gArgs

    hubTimeArray= np.empty(0)
    counterArray= np.empty(0)
    distanceArray= np.empty(0)
    fpidxArray= np.empty(0)
    overallrxpArray= np.empty(0)
    fppArray= np.empty(0)

    print ("Python version:"+sys.version)

    if gArgs.file:
        with open(gArgs.file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if(row[1]=="U3"):
                    #print("Hub Time:",row[2])
                    hubTimeArray = np.append(hubTimeArray, int(row[2]))
                    #print("Ranging counter:",row[3])
                    counterArray = np.append(counterArray, int(row[3]))
                    #print("json:",row[4])
                    try:
                        parsedData = json.loads(row[4])
                        if gArgs.anchor:
                            #print("Distance:",parsedData[gArgs.anchor]["d"])
                            distanceArray = np.append(distanceArray, float(parsedData[gArgs.anchor]["d"]))
                            fpidxArray = np.append(fpidxArray, float(parsedData[gArgs.anchor]["dt"]))
                            overallrxpArray = np.append(overallrxpArray, float(parsedData[gArgs.anchor]["snr"]))
                            fppArray = np.append(fppArray, float(parsedData[gArgs.anchor]["dPow"]))

                    except json.decoder.JSONDecodeError:
                        print("Error on incomplete line")

            #Create the dataframe
            #print("hubTimeArray.size:", hubTimeArray.size,"counterArray.size:", counterArray.size,"distanceArray.size:", distanceArray.size,"fpidxArray.size:", fpidxArray.size,"overallrxpArray.size:", overallrxpArray.size,"fppArray.size:", fppArray.size, )
            df = pandas.DataFrame({'Timestamp':hubTimeArray,'RangingCounter':counterArray, 'Distance': distanceArray, 'FirstPathIndex':fpidxArray, 'OverallRxPower': overallrxpArray, 'FirstPathPower': fppArray })
            #print(df)
            #plt.figure()
            df.plot(x='Timestamp', y='Distance')
            df.plot(x='Timestamp', y='FirstPathIndex')
            df.plot(x='Timestamp', y='OverallRxPower')
            df.plot(x='Timestamp', y='FirstPathPower')
            plt.show()
            

        #print("hubTimeArray:",hubTimeArray)

    #writer = csv.writer(outcsv)
    #writer.writerow(["Date", "temperature 1", "Temperature 2"])

    print ("Script Terminated")

####################
if __name__ == "__main__":
    handle_main_arg()
    main()
