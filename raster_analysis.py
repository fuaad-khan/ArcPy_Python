#Author: Fuaad Khan
#Date: November 17, 2019
#
#Purpose:  practice raster manipulation using the ArcPy Spatial Analyst module.
#          This will include describing raster properties, accessing raster data,
#          calculating rasters, and reclassifying rasters.

#Import Libraries
import arcpy
import os
import math
from arcpy.sa import *

#Set working directory
folderPath = r"C:\Users\Fuaad Khan\Desktop\LabData"

#Set environment path and overwrite
arcpy.env.workspace = folderPath
arcpy.env.overwriteOutput = True

#Part 1: Print out the following properties of the image: size of the image (number of pixels X and Y),
#resolution (units), map projection name, and the number of bands;

landsat = "Landsat.tif"

#Print out the number of pixels X and Y as well as the map's resolution
desc = arcpy.Describe(landsat + '/Band_1')
print("Height (Y Pixels):" + str(desc.height))
print("Width (X Pixels):" + str(desc.width))
print("Size of Image (Resolution):" + str(desc.meanCellHeight)+ " " + str(desc.spatialReference.linearUnitName)+ "s")

#Print out the Map Projection and number of bands
desc = arcpy.Describe(landsat)
print(landsat + "'s Map Projection: " + desc.spatialReference.Name)
print("Number of Bands:" + str(desc.bandCount))

#initialize raster ouput
o_raster = os.path.join(folderPath, "landsat_output.shp")

#Part 2: Compute an NDVI raster using the appropriate band combo
if arcpy.CheckOutExtension("Spatial") == "CheckedOut":
    #Assign a variable to the red and Infrared band for future raser calculation
    Red = arcpy.Raster(landsat +'/Band_3')
    Infrared = arcpy.Raster(landsat +'/Band_4')

    #Convert band to float and save as .TIF
    Red_float  = arcpy.sa.Float(Red) 
    Red_float.save("landsat_Red.TIF")
    print("landsat_Red.TIF created...")
    Infrared_float = arcpy.sa.Float(Infrared)
    Infrared_float.save("landsat_Infrared.TIF")
    print("landsat_Infrared.TIF created...")
        
    #Perform NDVI Calculation
    o_raster = (Infrared_float - Red_float) / (Red_float + Infrared_float)
    print("NDVI Calculated...")
    o_raster.save("landsat_NDVI.TIF")
    print("landsat_NDVI.TIF created...")

#Part 3: Generate an NDVI category raster using the following ranges:
#1 for values <= 0.0
#2 for values > 0.0 and <= 0.3
#3 for values >0.3

NDVI = "landsat_NDVI.TIF"
remap = arcpy.sa.RemapRange([[-0.7,0,1],[0,0.3,2], [0.3,1, 3]])
o_Remap = Reclassify(NDVI, "Value", remap)
o_Remap.save("landsat_Reclassified.TIF")
print("Reclassification complete")

#Part 4: Output the NDVI value and associated categorical value at the location (349908,3768856)
NDVI_Value = arcpy.GetCellValue_management("landsat_Reclassified.TIF", "349908 3768856", "1")
cat_Value = arcpy.GetCellValue_management(NDVI, "349908 3768856", "1")
ndvi = NDVI_Value.getOutput(0)
category = cat_Value.getOutput(0)

print("At the coordinates (349908 3768856) the cell value is  " + category+ " and the NDVI value is " +ndvi)
                      
#Cleanup
del NDVI, remap, landsat

