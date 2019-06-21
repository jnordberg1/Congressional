# -*- coding: utf-8 -*-


import arcpy
import os
from arcpy import env
import pandas  as pd


env.overwriteOutput     =   True 
#cwd = os.getcwd()!
env.workspace = r'C:\USS\United States Solar Corporation\Site Selection - Documents\Data\State\MN\Source\shp_bdry_housedistricts2012' #=cwd

in_spread               =   'meminfo.xls'
in_shp                  =   'hse2012_vtd2016.shp'
out_csv                  =   'meminfo.csv'
out_shp                 =   'MN_House_2019.shp'
phi                     =   "DeleteTemp"      

pd.read_excel(os.path.join(env.workspace, in_spread), sheet_name='2019_20_MemberInformation_for_W').to_csv(os.path.join(env.workspace, out_csv), index=False)

arcpy.TableToTable_conversion(out_csv, "in_memory", phi)
arcpy.CopyFeatures_management(in_shp, out_shp)


join_fields = ['fname', 'lname', 'partypol']
arcpy.JoinField_management(out_shp, "district", os.path.join("in_memory", phi), "district_id", join_fields)

arcpy.CalculateField_management(out_shp, 'name', '!fname!+" "+!lname!', 'PYTHON_9.3')
arcpy.CalculateField_management(out_shp, 'party', '!partypol!', 'PYTHON_9.3')

arcpy.DeleteField_management(out_shp, ["memid", "fname","lname", "partypol"])
arcpy.Delete_management(os.path.join("in_memory", phi))
