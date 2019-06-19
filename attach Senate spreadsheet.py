# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 12:00:24 2019

@author: JacobNordberg
"""
import arcpy
import os
from arcpy import env

env.overwriteOutput     =   True 
#cwd = os.getcwd()!
env.workspace = r'C:\USS\United States Solar Corporation\Site Selection - Documents\Data\State\MN\Source\shp_bdry_senatedistricts2012' #=cwd

in_csv                  =   'ascii_senators.csv'
in_shp                  =   'sen2012_vtd2016.shp'
out_shp                 =   'MN_Senate_2019.shp'
phi                     =   "DeleteTemp"      
        
arcpy.TableToTable_conversion(in_csv, "in_memory", phi)
arcpy.CopyFeatures_management(in_shp, out_shp)
arcpy.AddField_management(out_shp, "District_1", "LONG")
arcpy.CalculateField_management(out_shp, "District_1", '!MNSENDIST!', "PYTHON_9.3")

join_fields = ['Last_Name', 'First_Name', 'Party']
arcpy.JoinField_management(out_shp, "District_1", os.path.join("in_memory", phi), "District", join_fields)

arcpy.CalculateField_management(out_shp, 'name', '!First_Name!+" "+!Last_Name!', 'PYTHON_9.3')
arcpy.CalculateField_management(out_shp, 'party', '!Party_1!', 'PYTHON_9.3')

arcpy.DeleteField_management(out_shp, ["District_1", "memid", "First_Name", "Last_Name", "Party_1"])
arcpy.Delete_management(os.path.join("in_memory", phi))
