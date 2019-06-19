# -*- coding: utf-8 -*-


import arcpy
import os
from arcpy import env
import pandas  as pd


env.overwriteOutput     =   True 
#cwd = os.getcwd()!
env.workspace = r'C:\USS\United States Solar Corporation\Site Selection - Documents\Data\State\MN\Source\shp_bdry_housedistricts2012' #=cwd

in_csv                  =   'meminfo.csv'
in_shp                  =   'hse2012_vtd2016.shp'
out_shp                 =   'MN_House_2019.shp'
phi                     =   "DeleteTemp"      



pd.read_excel(env.workspace+'\meminfo.xls', sheet_name='2019_20_MemberInformation_for_W').to_csv(env.workspace+"\\"+in_csv, index=False)

arcpy.TableToTable_conversion(in_csv, "in_memory", phi)
arcpy.CopyFeatures_management(in_shp, out_shp)


join_fields = ['district_id', 'fname', 'lname', 'partypol']
arcpy.JoinField_management(out_shp, "district", os.path.join("in_memory", phi), "district_id", join_fields)

arcpy.CalculateField_management(out_shp, 'name', '!fname!+" "+!lname!', 'PYTHON_9.3') #<-- this would be easier if you picked better names in your scraping
arcpy.CalculateField_management(out_shp, 'party', '!partypol!', 'PYTHON_9.3') #<-- this would be easier if you picked better names in your scraping

arcpy.DeleteField_management(out_shp, ["memid", "fname","lname", "partypol", "district_i"])
arcpy.Delete_management(os.path.join("in_memory", phi))
