#Author: Fuaad Khan
#Date: October 19, 2019
#
#Purpose: This tool takes in 4 inputs: A Lake shape file,
#         City shape file, Proximity value, and a Country shape file.
#         Outputs table with simple statistics

#import Arcpy
import os
import arcpy

#Allow Overwrite
arcpy.env.overwriteOutput = True

#Input parameters
in_lake = arcpy.GetParameterAsText(0)
in_city = arcpy.GetParameterAsText(3)  
in_NA = arcpy.GetParameterAsText(6) 
prx_val = arcpy.GetParameterAsText(2)

#Output parameters
o_lakeBuffer = arcpy.GetParameterAsText(1)   
o_selected_cities =arcpy.GetParameterAsText(4) 
o_table = arcpy.GetParameterAsText(5)

#Buffer Analysis 
arcpy.Buffer_analysis(in_lake, o_lakeBuffer, prx_val, '', '', '', '', '')
print("Buffer Complete")

#Clip Cities in Buffer area
arcpy.Clip_analysis(in_city, o_lakeBuffer, o_selected_cities, '')
print("Clipped")

#Simple statistics based on Country
arcpy.Statistics_analysis(o_selected_cities, o_table, statistics_fields="Population SUM", case_field="CNTRY_NAME")
print("Summary Done")

#Join country population to result table
arcpy.JoinField_management(o_table, "CNTRY_NAME", in_NA, "CNTRY_NAME", "POP_CNTRY")
print("Joined")

#Add Field for Population Percentage
arcpy.AddField_management(o_table, "Pop_Prcnt", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("Added Field")

#Calculate the Population Percentage
arcpy.CalculateField_management(o_table, "Pop_Prcnt", "([SUM_Population] / [POP_CNTRY]) *100", "VB", "")
print("Population % Calculated")
