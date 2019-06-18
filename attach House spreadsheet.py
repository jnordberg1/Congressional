# -*- coding: utf-8 -*-

import arcpy
from arcpy import env

env.workspace           =   r''
env.overwriteOutput     =   True
in_csv                  =   r'C:\USS\United States Solar Corporation\Site Selection - Documents\Data\State\MN\Source\shp_bdry_housedistricts2012\HouseMembers.csv'
in_shp                  =   r'C:\USS\United States Solar Corporation\Site Selection - Documents\Data\State\MN\Source\shp_bdry_housedistricts2012\hse2012_vtd2016.shp'
out_table               =   r'C:\Users\JacobNordberg\Documents\ArcGIS\Default.gdb'
out_shp                 =   "Updated_House"
phi                     =   "DeleteTemp"
        
        
arcpy.TableToTable_conversion(in_csv, out_table, "HouseUpdate" + phi)
arcpy.CopyFeatures_management(in_shp, "NMCongressional"+phi)
join_fields = ['House_Member', 'District', 'Party', 'Office_Address', 'City_State_Zip', 'Phone_Number', 'Email']
arcpy.JoinField_management("NMCongressional"+phi, "MNLEGDIST", "HouseUpdate"+ phi, "District", join_fields)
arcpy.CopyFeatures_management("NMCongressional"+phi, out_shp)
arcpy.DeleteField_management(out_shp, ["district", "party", "name"])
arcpy.Delete_management("NMCongressional"+phi)
arcpy.Delete_management("HouseUpdate" + phi)