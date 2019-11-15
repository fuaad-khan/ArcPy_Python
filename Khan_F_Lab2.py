#Author: Fuaad Khan
#Date: Octobeer 13, 2019
#
#Purpose:   Runs a 100,000 meter Buffer analysis around the NA_Cities shapefile.
#           Runs a Clip analysis on the new buffer shapefile and NA_Big_lakes shapefile. 
#           Prints and counts the number of files in the directory.
#           Prints the categories of the file extensions

#Definition of file path
folderPath= r'C:\Users\Fuaad Khan\Desktop\Lab2\LabData'

#Import Libraries
import os
import arcpy

#Set up and define workspace
arcpy.env.workspace = folderPath

#Allow overwriting
arcpy.env.overwriteOutput = True

#Execute Buffer Analysis
print("Launching Buffer Analysis of 100,000 meters around NA_Cities.shp...")

arcpy.Buffer_analysis("NA_Cities.shp", os.path.join(folderPath,"Buffer.shp"), "100000 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field="", method="PLANAR")
print("Buffer Analysis Complete")

#Execute Clip Analysis
print("Launching Clip Analysis of buffer file...")
arcpy.Clip_analysis("Buffer.shp", "NA_Big_Lakes.shp", os.path.join(folderPath,"Buffer_Clip.shp"), cluster_tolerance="0 Meters")
print("Clip Analysis Complete"+"\n")

#variable used to identify the number of file
a = 1

#creating an object list for the files in the directory
dirs = os.listdir(folderPath)

#loop through and print all the files
for file in dirs:
    print (str(a)+": "+file)
    a = a +1

#adjust variable to calculate total files
a = a-1

#prints file to the console
print("There is a total number of "+str(a)+" files in this directory")

#Create a list where I can put the shapefiles
shp_list = []
for f in dirs:
    if f.endswith('.shp'):
        shp_list.append(f) 

#Print number of shapefiles
print ("\n"+"There are " + str(len(shp_list)) + " shapefiles in this directory.")
print (shp_list)

#Create a list where I can put the dbf files
dbf_list = []
for f in dirs:
    if f.endswith('.dbf'):
        dbf_list.append(f)

print ("\n"+"There are " + str(len(dbf_list)) + " dbf files in this directory.")
print (dbf_list)

#Create a list where I can put the tif files
tif_list = []
for f in dirs:
    if f.endswith('.tif'):
        tif_list.append(f)

print ("\n"+"There are " + str(len(tif_list)) + " tif files in this directory.")
print (tif_list)

#Create a list where I can put the xml files
xml_list = []
for f in dirs:
    if f.endswith('.xml'):
        xml_list.append(f)

print ("\n"+"There is " + str(len(xml_list)) + " xml file in this directory.")
print (xml_list)

#Create a list where I can put the mxd files
mxd_list = []
for f in dirs:
    if f.endswith('.mxd'):
        mxd_list.append(f)

print ("\n"+"There is " + str(len(mxd_list)) + " mxd file in this directory.")
print (mxd_list)


