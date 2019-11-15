#Author: Fuaad Khan
#Date: November 4, 2019
#
#Purpose: This tool takes in 2 inputs: A Lake shapefile and a city shapefile.
#         Outputs the lake shapefile with all geometric features, retaining
#         the original field attributes, and adds 7 new fields(city name, city
#         country, city administrative name, city population, city x/y coordinates,
#         and the distance to the lake centroid*). Thes new fields are from the
#         closest city to the centroid from each lake.

#Import libraries
import arcpy
import math
import os

#Set directory
folderPath = arcpy.GetParameterAsText(0)

#Allow Overwrite
arcpy.env.overwriteOutput = True

#User specified lake and city inputs
inLake = arcpy.GetParameterAsText(1)
inCity = arcpy.GetParameterAsText(2)

#User specified output location
output = arcpy.GetParameterAsText(3)

#Copy shapefiles and add to the working directory
lake_shape = os.path.join(folderPath, inLake)
city_shape = os.path.join(folderPath, inCity)
arcpy.CopyFeatures_management(lake_shape, output)


#This is the copied lake shapefile with the user's output location
newLake = os.path.join(folderPath, output)

#The 7 new fields added to the newLake output shapefile
arcpy.AddField_management(newLake, "City_Name", "TEXT")
arcpy.AddField_management(newLake, "City_Cntry", "TEXT")
arcpy.AddField_management(newLake, "Admin_Name", "TEXT")
arcpy.AddField_management(newLake, "City_Pop", "LONG")
arcpy.AddField_management(newLake, "City_X", "FLOAT")
arcpy.AddField_management(newLake, "City_Y", "FLOAT")
arcpy.AddField_management(newLake, "Centr_Dist", "FLOAT")

#Initialize lists to hold the city information
listCity_Name = []
listCity_Cntry = []
listAdmin_Name = []
listCity_Pop = []
listCity_X = []
listCity_Y = []
listCentroid_Dist = []

#Create a search cursor to find the first new 6 fields and add it to our empty lists
fields = ["CITY_NAME", "CNTRY_NAME","ADMIN_NAME", "Population","SHAPE@XY"]
field_search = arcpy.da.SearchCursor(city_shape, fields)
for field in field_search:
    #appends to empty lists
    listCity_Name.append(field[0])
    listCity_Cntry.append(field[1])
    listAdmin_Name.append(field[2])
    listCity_Pop.append(field[3])
    #needs two indexes because SHAPE@XY is a tuple
    listCity_X.append(field[4][0])
    listCity_Y.append(field[4][1])

#Create an update cursor and add all 7 fields to be updated
uFields = ["SHAPE@XY", "City_Name", "City_Cntry", "Admin_Name", "City_Pop", "City_X", "City_Y", "Centr_Dist"]
field_update = arcpy.da.UpdateCursor(newLake, uFields)


#Loop through the update cursor
for field in field_update:
    #finding the longitude/lattitude for the lakes from the SHAPE@XY in the uFields
    longLake = field[0][0] 
    latLake = field[0][1]
    #Initialzize a list to store distances
    distances_list = []
    #Loop through the range of cities appended to the empty lists
    for city in range(0, len(listCity_Name)):
        #Assign Longitude/Latitude city values from out appended list
        longCity = listCity_X[city]
        latCity = listCity_Y[city]

        #Calculate distance from the centroid of the lake to the cities
        distance = math.sqrt(((longLake - longCity)**2) + ((latLake - latCity)**2))
        #Add these calcualtions to our list that stores distance
        distances_list.append(distance)
        
    #Use a function that allows us to find the city with the least amount of distance i.e. closest city
    closestCity= min(distances_list)

    #Create an index and assign the proper index to the update field
    closestCityIndex = distances_list.index(closestCity) 
    field[1] = listCity_Name[closestCityIndex] 
    field[2] = listCity_Cntry[closestCityIndex]
    field[3] = listAdmin_Name[closestCityIndex]
    field[4] = listCity_Pop[closestCityIndex]
    field[5] = listCity_X[closestCityIndex]
    field[6] = listCity_Y[closestCityIndex]
    #Convert meters -> kilometers
    field[7] = closestCity *(.001)

    #Update these values
    field_update.updateRow(field)

#cleanup
del field_search
del field_update

    
