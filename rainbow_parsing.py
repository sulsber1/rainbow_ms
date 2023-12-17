import rainbow as rb
import os

datadir = rb.read("C:\\Users\\sulsb\\OneDrive\\Desktop\\github\\rainbow\\rainbow\\tests\\inputs\\blue.raw")


for datafile in datadir.datafiles:
    print(datafile.name, datafile.detector, datafile.get_info())
    #print(datafile.data)

#print(datadir.get_info())