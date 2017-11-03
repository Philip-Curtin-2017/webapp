#!flask/bin/python
from app import db, models


vote_list = []


votes = models.Vote.query.all()
finished_craters = 0
total_votes = 0
total_yes = 0
total_no = 0
total_border = 0
total_recenter = 0
total_unsure = 0
total_review = 0
total_SU = 0

for i, val in enumerate(votes):
    if not votes[i].crater_id in vote_list:
        vote_list.append(votes[i].crater_id)


    

for n, val in enumerate(vote_list):
    v_num = 0
    y_num = 0
    n_num = 0
    u_num = 0
    r_num = 0

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
                print("Recenter crater {}: ({},{}), ({},{}) z-score: {}".format(votes[x].crater_id, 
                                                                    votes[x].x1_new, 
                                                                    votes[x].y1_new, 
                                                                    votes[x].x2_new, 
                                                                    votes[x].y2_new,
                                                                    votes[x].recenter_zscore))
            if votes[x].vote_type == 'super_user_vote':
                total_SU +=1

    if v_num >= 15:
        finished_craters += 1
        if (y_num >= 10):
            total_yes += 1
        elif (n_num >= 10):
            total_no += 1
        elif ( u_num >= 10):
            total_unsure += 1
        elif (((y_num + r_num) >= 6) and (n_num >= 6)):
            total_border += 1
        elif (((r_num + y_num) >= 10) and (r_num >= 5)):
            total_recenter += 1
        else:
            total_review += 1
    total_votes += v_num
 
    print("______ Result Crater ID {}: Yes: {}, No: {}, Unsure: {}, Re_Center: {}, Total: {}".format(vote_list[n],
                                                                                        y_num,
                                                                                        n_num,
                                                                                        u_num,
                                                                                        r_num,
                                                                                        v_num))

print("{} total craters evaluated".format(len(vote_list)))
print("Finished craters: {}, total votes: {}".format(finished_craters, total_votes))
print("Totals: Yes: {}, No: {}, Recenter: {}, Unsure: {}, Border-line: {}, Review: {}, Super User Votes: {} ".format(total_yes, 
                                                                                    total_no, 
                                                                                    total_recenter,
                                                                                    total_unsure,
                                                                                    total_border,
                                                                                    total_review,
                                                                                    total_SU))





