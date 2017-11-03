#!flask/bin/python
from app import db, models
from sqlalchemy import and_
#this script evaluates the collected votes and assigns the result status to the corresponding CDA entry.
#CDA entries that have already been evaluated will not be re-evaluated

vote_list = []


votes = models.Vote.query.all()
finished_craters = 0
total_votes = 0

#get list of CDA ids from votes
print("generating vote list")
for i, val in enumerate(votes):
    if not votes[i].crater_id in vote_list:
        vote_list.append(votes[i].crater_id)

#evaluate votes for each id in the list
print("counting votes")
for n, val in enumerate(vote_list):
    v_num = 0
    y_num = 0
    n_num = 0
    u_num = 0
    r_num = 0
    SU_num = 0
    result = 'none'

    #count votes to make sure only completed entries are modified
    entries=models.CDA.query.get(vote_list[n])
    print("crater id {}".format(entries.id))
    if (entries.vote_result == None):
        for x, val in enumerate(votes):
            if votes[x].crater_id == vote_list[n]:
                v_num += 1
                if votes[x].vote_result == 'yes':
                    y_num +=1
                elif votes[x].vote_result == 'no':
                    n_num +=1
                elif votes[x].vote_result == 'unsure':
                    u_num +=1
                elif votes[x].vote_result == 'recenter':
                    r_num +=1
                if votes[x].vote_type =='super_user_vote':
                    SU_num +=1


                    
        #record results: all unsure, borderline, and exception results are recorded as 'review' for super user evaluation
        if v_num >= 15:
            
            if (y_num >= 10):
                result = 'yes'
            elif (n_num >= 10):
                result = 'no'
            elif ( u_num >= 10):
                result = 'review'
            elif (((r_num + y_num) >= 10) and (r_num >= 5)):
                result = 'recenter'
            else:
                result = 'review'
            entries.vote_result = result

            print("Crater ID {}: Vote result {}: yes {}: no {}: unsure {}: recenter {}: SU {}".format(entries.id, 
                                                                                                        entries.vote_result,
                                                                                                        entries.results_yes,
                                                                                                        entries.results_no,
                                                                                                        entries.results_unsure,
                                                                                                        entries.results_recenter,
                                                                                                        entries.results_SU_vote))
            db.session.add(entries)
print('Committing vote results')
db.session.commit()
db.session.remove()

#determine appropriate recenter vote to use as the entry on "recenter" status CDA entries
print('Querrying recenter results')
recenters = models.CDA.query.filter(and_(models.CDA.vote_result == 'recenter', models.CDA.recenter_id == None))
for recenter_entry in recenters:
    print('recentered crater id is {}'.format(recenter_entry.id))
    temp_id = recenter_entry.id
    recenter_votes = models.Vote.query.filter(and_(models.Vote.crater_id == temp_id, models.Vote.vote_result == 'recenter'))

    num = 0.0
    total_x = 0.0
    total_y = 0.0
    mean_x = 0.0
    mean_y = 0.0
    varience_total_x = 0.0
    varience_total_y = 0.0
    stddev_x = 0.0
    stddev_y = 0.0
    z_score = 1000000.0
    recenter_id = 0

    for a, val in enumerate(recenter_votes):
        print("Crater ID {}: Vote ID {}: num {}".format(recenter_votes[a].crater_id, recenter_votes[a].id, num))
        num += 1
        total_x += recenter_votes[a].x1_new
        total_y += recenter_votes[a].y1_new
    print("total-x {}, num {}".format(total_x, num))
    mean_x = (total_x/num)
    mean_y = (total_y/num)

    for b, val in enumerate(recenter_votes):
        varience_total_x += (recenter_votes[b].x1_new - mean_x)**2
        varience_total_y += (recenter_votes[b].y1_new - mean_y)**2

    stddev_x = ((varience_total_x/num)**0.5)
    stddev_y = ((varience_total_y/num)**0.5) 
    print("StdDev: x - {}, y - {}".format(stddev_x,stddev_y))
#find the lowest combined z-score for the x y recenter votes, and assign that vote as the new location.
    for c, val in enumerate(recenter_votes):
        try:
            tempx = abs((recenter_votes[c].x1_new-mean_x)/stddev_x)
        except: 
            print("divide by zero error, StdDev_x is {}".format(stddev_x))
            tempx = 0.0
        try:
            tempy = abs((recenter_votes[c].y1_new-mean_y)/stddev_y)
        except:
            print("divide by zero error, StdDev_y is {}".format(stddev_y))
            tempy = 0.0
        temp_zscore = tempx + tempy
        recenter_votes[c].recenter_zscore = temp_zscore
        db.session.add(recenter_votes[c])
        if (temp_zscore < z_score):
            z_score = temp_zscore
            recenter_id = recenter_votes[c].id
            print('recenter crater ID: {}, to location ({},{}), combined z-score of {}'.format(recenter_votes[c].crater_id,
                                                                                                recenter_votes[c].x1_new,
                                                                                                recenter_votes[c].y1_new,
                                                                                                z_score))

    recenter_entry.recenter_id = recenter_id
    db.session.add(recenter_entry)
print('Committing recenter location')
db.session.commit()



