#!/usr/bin/python
import zipfile
import os
import xmltodict
import json
import glob
import psycopg2
import shutil
import collections
# from insertGeometry import insert_coordinates
from insertStandEstimation import insert_stand_estimation
from credentials import cr_dbname, cr_host, cr_password, cr_user
# from insertAction1 import insert_action1
# from insertAction2 import insert_action2
# from insertStandEstimation import newId

path = "/home/r89/_projects/forest_python/incoming/*.collect-data"
# path = "/home/caiag/script/incoming/*.collect-data"

for filename in glob.glob(path):
    if 'oopt' in filename:
        newFilename = filename
        zf = zipfile.ZipFile(filename, 'r')
        jsonNumber = 1
        for name in zf.namelist():
            if name.endswith('/'):
                continue
            if 'data/' in name:
                f = zf.open(name).read() 
                newDict = xmltodict.parse(f, force_list={'forest_composition', 'forest_use_type', 'planned_forest_use_type', 'action_priority_1', 'tillage_1', 'creation_type_1', 'ecoproblems', 'plant_redflag', 'animal_redflag', 'main_plants'})
            
                with open(filename+str(jsonNumber)+'.json', 'w') as outfile:
                    json.dump(newDict, outfile, indent=4)
                
                insert_stand_estimation(newDict)
                jsonNumber = jsonNumber+1
    else: continue