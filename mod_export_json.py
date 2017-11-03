#!flask/bin/python
from app import db, models
from sqlalchemy import and_, or_

#This module creates a JSON file that can be used by the crater detection algorithm.
#the generated file will be in the webapp/data/jsons directory

#use this field to select the file name for the exported JSON
json_filename = 'default_json_filename'


#*************************************************
#       This code should not be altered
#*************************************************

#empty list to hold images's of finished craters
image_list = []
json_file_path = 'data/jsons/' + json_filename






print("generating image list")
GT = models.GroundTruth.query.all()
for a, val in enumerate(GT):
    if not GT[a].image in image_list:
        image_list.append(GT[a].image)


print('starting export')
first_entry_flag = True


jsonfile = open(json_file_path,'w')


# write the opening parentheses to the file
jsonfile.write('[')

#cycle through image list, printing all corresponding GT's and evaluated crater predictions
for b, val in enumerate(image_list):
    print('processing record {} of {}'.format(b,len(image_list)))

    GT_short = models.GroundTruth.query.filter(models.GroundTruth.image == image_list[b])
    CDA_short = models.CDA.query.filter(and_((models.CDA.image == image_list[b]),
                                        (or_(models.CDA.vote_result == 'yes', models.CDA.vote_result == 'recenter'))))

    
    if first_entry_flag == False:
        jsonfile.write(',')

    jsonfile.write('\n{{\n"image_path": "{}",\n"rects": ['.format(image_list[b]))
    first_entry_flag = True
    for GT_entry in GT_short:
        if first_entry_flag == False:
            jsonfile.write(',')
        first_entry_flag = False
        jsonfile.write('\n{\n')
        jsonfile.write('"x1": {}.0,\n'.format(GT_entry.x1))
        jsonfile.write('"x2": {}.0,\n'.format(GT_entry.x2))
        jsonfile.write('"y1": {}.0,\n'.format(GT_entry.y1))
        jsonfile.write('"y2": {}.0\n'.format(GT_entry.y2))
        jsonfile.write('}')

    if (type(CDA_short) != None): 
        for CDA_entry in CDA_short:
            if CDA_entry.vote_result == 'yes':
                x1 = CDA_entry.x1
                y1 = CDA_entry.y1
                x2 = CDA_entry.x2
                y2 = CDA_entry.y2

            elif CDA_entry.vote_result == 'recenter':
                recenter = models.Vote.query.get(CDA_entry.recenter_id)
                x1 = recenter.x1_new
                y1 = recenter.y1_new
                x2 = recenter.x2_new
                y2 = recenter.y2_new

            jsonfile.write(',\n{\n')
            jsonfile.write('"x1": {}.0,\n'.format(x1))
            jsonfile.write('"x2": {}.0,\n'.format(x2))
            jsonfile.write('"y1": {}.0,\n'.format(y1))
            jsonfile.write('"y2": {}.0\n'.format(y2))
            jsonfile.write('}')

    jsonfile.write('\n]\n}')



jsonfile.write('\n]')

jsonfile.close()


