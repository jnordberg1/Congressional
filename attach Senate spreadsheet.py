# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 12:00:24 2019

@author: JacobNordberg
"""
import arcpy
from arcpy import env

env.workspace           =   r''
env.overwriteOutput     =   True
in_csv                  =   r'C:\USS\United States Solar Corporation\Site Selection - Documents\Data\State\MN\Source\shp_bdry_senatedistricts2012\SenateMembers.csv'
in_shp                  =   r'C:\USS\United States Solar Corporation\Site Selection - Documents\Data\State\MN\Source\shp_bdry_senatedistricts2012\sen2012_vtd2016.shp'
out_table               =   r'C:\Users\JacobNordberg\Documents\ArcGIS\Default.gdb'
out_shp                 =   r'C:\USS\United States Solar Corporation\Site Selection - Documents\Data\State\MN\Source\shp_bdry_senatedistricts2012\Updated_Senate.shp'
phi                     =   "DeleteTemp"
        
        
arcpy.TableToTable_conversion(in_csv, out_table, "SenateUpdate" + phi)
arcpy.AddField_management(in_shp, "District_1", "LONG")
arcpy.CalculateField_management(in_shp, "District_1", '!MNSENDIST!', "PYTHON_9.3")
arcpy.CopyFeatures_management(in_shp, "NMCongressional"+phi)
join_fields = ['Senator', 'District', 'Party', 'Office_Address', 'City_State_Zip', 'Phone_Number', 'Email']
arcpy.JoinField_management("NMCongressional"+phi, "District_1", "SenateUpdate"+ phi, "District", join_fields)
arcpy.CopyFeatures_management("NMCongressional"+phi, out_shp)
arcpy.DeleteField_management(out_shp, ["district", "party", "name", "District_1", "Shape_Leng", "OBJECTID"])
arcpy.Delete_management("NMCongressional"+phi)
arcpy.Delete_management("SenateUpdate" + phi)