# Author: Fuaad Khan
# Date: October 28, 2019
#
# Purpose: Create a new lab4.gdb if one does not ALready exist. Add a table to the GDB named Lab_Week4. 
#          Add records for US and Mexican cities with population >= 8,000,000 and Canadian cities with Population >= 3,000,000 

#Workspace and file directory
folderPath = r"C:\Users\Fuaad Khan\Desktop\Lab4\LabData"

#Import libraries/modules
import arcpy
import os

#Establish Workspace
arcpy.env.workspace = folderPath
arcpy.env.overwriteOutput = True

#Create list of files in directory
dirs = os.listdir(folderPath)

#Create a variable for the new GDB
new_gdb = "lab4.gdb"

#Check whether or not this GDB exists, if not create it
if new_gdb not in dirs:
    arcpy.CreateFileGDB_management(folderPath, new_gdb)
    print("New GDB lab4.gdb was created in directory...")

#Create new Table in lab4.gdb
arcpy.CreateTable_management(folderPath+"\lab4.gdb", "Lab_Week4")
arcpy.AddField_management(folderPath+"\lab4.gdb\Lab_Week4", "city_name", "TEXT")
arcpy.AddField_management(folderPath+"\lab4.gdb\Lab_Week4", "cntry_name", "TEXT")
arcpy.AddField_management(folderPath+"\lab4.gdb\Lab_Week4", "admin_name", "TEXT")
arcpy.AddField_management(folderPath+"\lab4.gdb\Lab_Week4", "population", "TEXT")
print("New table Lab_Week4 created...")

#Create variable for feature class with data we wish to use
fc = "NA_Cities.shp"

#Establish the field we wish to add our delimited field/SQL where clause
field_pop = "population"

#Create delimited field to overcome complications with unknown delimiters and SQL
delim_pop = arcpy.AddFieldDelimiters(fc, field_pop)

#Search Cursor to find the rows we want for the US and Mexico
rows_USM = arcpy.da.SearchCursor(fc, ["city_name", "cntry_name","admin_name", "population"], delim_pop + " >= 8000000")

#Search Cursor to find the rows we want for canada
rows_Ca = arcpy.da.SearchCursor(fc, ["city_name", "cntry_name","admin_name", "population"], delim_pop + " >= 3000000")

#Insert Cursor for the new table
inCursor = arcpy.da.InsertCursor(folderPath+"\lab4.gdb\Lab_Week4", ["city_name", "cntry_name","admin_name", "population"])

#Loop through the first cursor to find the cities in the US and Mexico with Populations >= 8,000,000
for row in rows_USM:
    if row[1] == "United States":
        inCursor.insertRow([row[0], row[1], row[2], row[3]])
    elif row[1] == "Mexico":
        inCursor.insertRow([row[0], row[1], row[2], row[3]])
        
#Loop through the Second cursor to find cities in Canda with a population >= 3,000,000 
for ca_row in rows_Ca:
    if ca_row[1] == "Canada":
        inCursor.insertRow([ca_row[0], ca_row[1], ca_row[2], ca_row[3]])

#Update to user that the script is complete
print("Output Table Lab_Week4 has been updated")

#Cleanup and unlock cursors
del rows_USM
del inCursor
del rows_Ca
del row
del ca_row
