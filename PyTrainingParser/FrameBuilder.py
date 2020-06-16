import os
import pandas
import json
import numpy as np

class FrameBuilder:
    _file = ""
    _dataFrame = pandas.DataFrame()
  

    # TODO: make the list of d_x configurable
    def __init__(self, filename):
        self._file = open(filename, newline='')

    def getDataFrame(self):
        reader = csv.reader(self._file, delimiter=';')
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
        return self._dataFrame
