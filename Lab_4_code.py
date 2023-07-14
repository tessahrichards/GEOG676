import arcpy 

arcpy.env.workspace =r'"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"' #where ArcPy is stored on my local machine
folder_path =r'C:\GEOG_676_ENV' #folder including acrgis project file, garages csv and campus gdb
gdb_name = "Lab_4.gdb"
gdb_path = folder_path + '\\' + gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name)

csv_path = r"C:\GEOG_676_ENV\garages.csv"
garage_layer_name = 'Garage_Points'
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name

campus = r'C:\GEOG_676_ENV\Campus.gdb'
buildings_campus = campus + '\Structures'
buildings = gdb_path + '\\' + 'Buildings'

arcpy.Copy_management(buildings_campus, buildings)

spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_Reprojected', spatial_ref)

garageBuffered = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_Reprojected', gdb_path + '\Garage_Points_Buffered', 150)

arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Building_Intersection', 'ALL')
arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersection.dbf',r'C:\GEOG_676_ENV\Lab_4.gdb', 'nearbyBuildings.csv')

