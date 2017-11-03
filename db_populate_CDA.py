#!flask/bin/python
from app import db, models
import json
from pprint import pprint
from datetime import datetime
#This module is used to initially populate the CDA and Ground Truth databases, or
#to erase the existing databases and repopulate them with new data. See the README for more 
#information about this module and the required file format.




#set these flags to delete the Vote database, and repopulate the CDA and GT databases. 
#Set to True to delete / populate, False to skip.
populate_CDA = False
populate_GroundTruth = False
delete_votes = False

#name of JSON files in the 'jsons' directory, with CDA prediction data and ground truth data
#replace these filenames to erase the previous databases and populate with new data 
CDA_filename = "CDA_predictions_full.json"
GroundTruth_filename = "groundtruth_full.json"


#*******************************************************
#       This code should not be altered
#*******************************************************
CDA_file_path = 'data/jsons/'+CDA_filename
GroundTruth_file_path = 'data/jsons/'+GroundTruth_filename

if (populate_CDA == True):
    #Delete old CDA entries before importing new data 
    #commit every 500 as large commits crashed the server
    entries = models.CDA.query.all()
    n=0
    for entry in entries:
        db.session.delete(entry)
        n+=1
        if (n >= 500):
            db.session.commit()
            n=0
            print("commit")
    db.session.commit()


    #Open CDA file and populate the CDA database table
    with open(CDA_file_path) as data_file:
            objects = [ i for i in json.load(data_file) ]

    for i, val in enumerate(objects):
            for j, val in enumerate(objects[i]['rects']):
                    record = models.CDA(image=objects[i]['image_path'],
                    x1 = objects[i]['rects'][j]['x1'],
                    x2 = objects[i]['rects'][j]['x2'],
                    y1 = objects[i]['rects'][j]['y1'],
                    y2 = objects[i]['rects'][j]['y2'],
                    score = objects[i]['rects'][j]['score'],
                    timestamp = datetime.utcnow(),
                    GT_conflict = objects[i]['rects'][j]['GT_conflict'],
                    IOU = objects[i]['rects'][j]['IOU'],
                    var1 = "empty",
                    var2 = "empty")

                    db.session.add(record)
            print("commit")
            db.session.commit()
    db.session.commit()
    print("CDA populated")


if (populate_GroundTruth == True):
    #Delete old database entries before importing new data
    entries = models.GroundTruth.query.all()
    n=0
    for entry in entries:
        db.session.delete(entry)
        n+=1
        if (n >= 500):
            db.session.commit()
            n=0
            print("commit")
    db.session.commit()

    print("clear Ground Truth, begin populate GT")

    #Open CDA file and populate the CDA database table
    with open(GroundTruth_file_path) as data_file:
            objects = [ i for i in json.load(data_file) ]

    for i, val in enumerate(objects):
            for j, val in enumerate(objects[i]['rects']):
                    record = models.GroundTruth(image=objects[i]['image_path'],
                    x1 = objects[i]['rects'][j]['x1'],
                    x2 = objects[i]['rects'][j]['x2'],
                    y1 = objects[i]['rects'][j]['y1'],
                    y2 = objects[i]['rects'][j]['y2'])
                    db.session.add(record)
            print("commit")
            db.session.commit()
    db.session.commit()

    print("finished populate GT")

if (delete_votes == True):
    entries = models.Vote.query.all()
    n=0
    for entry in entries:
        db.session.delete(entry)
        n+=1
        if (n >= 500):
            db.session.commit()
            n=0
            print("commit")
    db.session.commit()
