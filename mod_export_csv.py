#!flask/bin/python
from app import db, models
from sqlalchemy import and_, or_
from datetime import datetime


#this module outputs csv files of the finished craters and the current votes to the webapp/data/csvs directory


#choose which databases to export, set to True to export, or False to skip
export_craters = True
export_votes = True

#change these fields to contain the filenames you want
crater_CSV_filename = 'crater_csv_10_2017'
votes_CSV_filename = 'vote_csv_10_2017'



#*************************************************
#       This code should not be altered
#*************************************************
#export crater CSV
if export_craters == True:

    print('starting predictions query')
    fin_craters = models.CDA.query.filter(models.CDA.vote_result != None).order_by(models.CDA.id)
    #fin_craters = models.CDA.query.all()

    #open file and write fields followed by recursively writing the crater entries
    print('writing csv document')
    crater_file_path = 'data/csvs/'+crater_CSV_filename+'.txt'
    f_crater = open(crater_file_path,'w')
    f_crater.write('id,image,x1,y1,x2,y2,score,IOU,vote_result,votes,votes_yes,votes_no,votes_unsure,votes_recenter,votes_SU,recenter_id,r_zscore,r_x1,r_y1,r_x2,r_y2\n')

    for crater in fin_craters:
        rx1 = None
        ry1 = None
        rx2 = None
        ry2 = None
        r_zscore = None

        if crater.vote_result == 'recenter':
            recenter = models.Vote.query.get(crater.recenter_id)
            rx1 = recenter.x1_new
            ry1 = recenter.y1_new
            rx2 = recenter.x2_new
            ry2 = recenter.y2_new
            r_zscore = recenter.recenter_zscore

        f_crater.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(crater.id,
                                                                                        crater.image,
                                                                                        crater.x1,
                                                                                        crater.y1,
                                                                                        crater.x2,
                                                                                        crater.y2,
                                                                                        crater.score,
                                                                                        crater.IOU,
                                                                                        crater.vote_result,
                                                                                        crater.votes,
                                                                                        crater.results_yes,
                                                                                        crater.results_no,
                                                                                        crater.results_unsure,
                                                                                        crater.results_recenter,
                                                                                        crater.results_SU_vote,
                                                                                        crater.recenter_id,
                                                                                        r_zscore,
                                                                                        rx1,
                                                                                        ry1,
                                                                                        rx2,
                                                                                        ry2))

    f_crater.close()

#export votes CSV
if export_votes == True:

    print('starting Votes query')
    current_votes = models.Vote.query.order_by(models.Vote.crater_id)

    #open file and write fields followed by recursively writing the crater entries
    print('writing csv document')
    votes_file_path = 'data/csvs/'+votes_CSV_filename+'.txt'
    f_votes = open(votes_file_path,'w')
    f_votes.write('crater id,vote id,result,z-score,x1_new,y1_new,x2_new,y2_new,session data,vote type, start timestamp, end timestamp, total seconds\n')

    for vote in current_votes:
        time_since = vote.end_timestamp - vote.start_timestamp
        num_seconds = int(time_since.total_seconds())


        f_votes.write('{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(vote.crater_id,
                                                                    vote.id,
                                                                    vote.vote_result,
                                                                    vote.recenter_zscore,
                                                                    vote.x1_new,
                                                                    vote.y1_new,
                                                                    vote.x2_new,
                                                                    vote.y2_new,                                                                    
                                                                    vote.session_data,                                                                    
                                                                    vote.vote_type,
                                                                    vote.start_timestamp,
                                                                    vote.end_timestamp,
                                                                    num_seconds))

    f_votes.close()
