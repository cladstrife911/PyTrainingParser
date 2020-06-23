import os
import pandas
import json
import numpy as np
import csv

class FrameBuilder:
    _filename = ""
    _dataFrame = pandas.DataFrame()
  
    #_hubTimeArray
    #_counterArray
    #_distanceArray
    #_fpidxArray
    #_overallrxpArray
    #_fppArray

    # TODO: make the list of d_x configurable
    def __init__(self, filename, anchorId="10"):
        self._filename = filename
        self._hubTimeArray= np.empty(0)
        self._counterArray= np.empty(0)
        self._distanceArray= np.empty(0)
        self._fpidxArray= np.empty(0)
        self._pRArray= np.empty(0)
        self._pFArray= np.empty(0)
        self._pMArray= np.empty(0)
        self._dIArray= np.empty(0)
        self._overallrxpArray= np.empty(0)
        self._fppArray= np.empty(0)
        self._anchorId= anchorId
        #populate the dataframe
        self.prepareDataFrame()
        
    def prepareDataFrame(self):
        with open(self._filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if(row[1]=="U3"):
                    version = "U3"
                    #print("Hub Time:",row[2])
                    #print("Ranging counter:",row[3])
                    #print("json:",row[4])
                    try:
                        parsedData = json.loads(row[4])
                        if self._anchorId:
                            self._hubTimeArray = np.append(self._hubTimeArray, int(row[2]))
                            self._counterArray = np.append(self._counterArray, int(row[3]))
                            #print("Distance:",parsedData[gArgs.anchor]["d"])
                            self._distanceArray = np.append(self._distanceArray, float(parsedData[self._anchorId]["d"]))
                            self._fpidxArray = np.append(self._fpidxArray, float(parsedData[self._anchorId]["dt"]))
                            self._overallrxpArray = np.append(self._overallrxpArray, float(parsedData[self._anchorId]["snr"]))
                            self._fppArray = np.append(self._fppArray, float(parsedData[self._anchorId]["dPow"]))
                    except json.decoder.JSONDecodeError:
                        print("Error on incomplete line")
                elif (row[1]=="U3.1"):
                    version = "U3.1"
                    try:
                        parsedData = json.loads(row[4])
                        if self._anchorId:
                            self._hubTimeArray = np.append(self._hubTimeArray, int(row[2]))
                            self._counterArray = np.append(self._counterArray, int(row[3]))
                            self._distanceArray = np.append(self._distanceArray, float(parsedData[self._anchorId]["d"]))
                            self._fpidxArray = np.append(self._fpidxArray, float(parsedData[self._anchorId]["iF"]))
                            self._overallrxpArray = np.append(self._overallrxpArray, float(parsedData[self._anchorId]["pR"]))
                            self._fppArray = np.append(self._fppArray, float(parsedData[self._anchorId]["pF"]))
                    except json.decoder.JSONDecodeError:
                        print("Error on incomplete line")
                elif (row[1]=="U3.2"):
                    version = "U3.2"
                    try:
                        parsedData = json.loads(row[4])
                        if self._anchorId:
                            self._hubTimeArray = np.append(self._hubTimeArray, int(row[2]))
                            self._counterArray = np.append(self._counterArray, int(row[3]))
                            self._distanceArray = np.append(self._distanceArray, float(parsedData[self._anchorId]["d"]))
                            self._pRArray = np.append(self._pRArray, float(parsedData[self._anchorId]["pR"]))
                            self._pFArray = np.append(self._pFArray, float(parsedData[self._anchorId]["pF"]))
                            self._pMArray = np.append(self._pMArray, float(parsedData[self._anchorId]["pM"]))
                            self._dIArray = np.append(self._dIArray, float(parsedData[self._anchorId]["dI"]))
                    except json.decoder.JSONDecodeError:
                        print("Error on incomplete line")

            #print(self._hubTimeArray.size, self._counterArray.size,self._distanceArray.size,self._fpidxArray.size,self._overallrxpArray.size,self._fppArray.size)
            if version == "U3.2":
                self._dataFrame = pandas.DataFrame({\
                    'Timestamp':self._hubTimeArray, \
                    'RangingCounter':self._counterArray, \
                    'Distance': self._distanceArray, \
                    'OverallRxPower': self._pRArray, \
                    'FirstPathPower': self._pFArray, \
                    'MaxPathPower': self._pMArray, \
                    'MaxPathVsEdgeIndex': self._dIArray })
            else:
                self._dataFrame = pandas.DataFrame({'Timestamp':self._hubTimeArray,'RangingCounter':self._counterArray, 'Distance': self._distanceArray, 'FirstPathIndex':self._fpidxArray, 'OverallRxPower': self._overallrxpArray, 'FirstPathPower': self._fppArray })
      
    def getDataFrame(self):
        return self._dataFrame

    def exportToCsv(self, outputfilename):
        self._dataFrame.to_csv(outputfilename, sep=';')
