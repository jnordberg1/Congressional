# -*- coding: utf-8 -*-


import arcpy
import os
from arcpy import env

env.overwriteOutput     =   True 
#cwd = os.getcwd()!
env.workspace = r'C:\USS\United States Solar Corporation\Site Selection - Documents\Data\State\MN\Source\shp_bdry_housedistricts2012' #=cwd

in_csv                  =   'HouseMembers.csv'
in_shp                  =   'hse2012_vtd2016.shp'
out_shp                 =   'MN_House_2019.shp'
phi                     =   "DeleteTemp"      
        
arcpy.TableToTable_conversion(in_csv, "in_memory", phi)
arcpy.CopyFeatures_management(in_shp, out_shp)

join_fields = ['House_Member', 'Party']
arcpy.JoinField_management(out_shp, "district", os.path.join("in_memory", phi), "District", join_fields)

arcpy.CalculateField_management(out_shp, 'name', '!House_Memb!', 'PYTHON_9.3') #<-- this would be easier if you picked better names in your scraping
arcpy.CalculateField_management(out_shp, 'party', '!Party_1!', 'PYTHON_9.3') #<-- this would be easier if you picked better names in your scraping

arcpy.DeleteField_management(out_shp, ["memid", "House_Memb", "Party_1"])
arcpy.Delete_management(os.path.join("in_memory", phi))
