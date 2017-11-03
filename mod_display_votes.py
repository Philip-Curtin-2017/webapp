#!flask/bin/python
from app import db, models
from sqlalchemy import and_, or_
from operator import itemgetter
from collections import namedtuple
from pprint import pprint
import numpy as np
import cv2 as cv

#This module is intended to put bounding boxes on images with fully evaluated craters.
#Additionally, two lists are printed to the terminal window. 
#first, a list of all images that contain completed CDA predictions, 
#in descending order of # of predictions, with the number of results
#second, a list of the images as they are being processed.



#set this value to "True" to make images, or "False" to only see the printed list in the terminal window
create_images = True


#Image secetion based on list printed to terminal window. This section only applies when "create_images = True"
#Use 'select type' to choose which images you want created. choices are 'all', 'individual', or 'range'
select_type = 'range'

#for "select_type = individual", 
#enter the desired 'list position' numbers from the list printed to the erminal window, for example [0,1,2,5,7,12]
select_individual_images = [1]

#for "select_type = range", enter the 'list position' numbers from the list printed to the terminal window,
#for example, 'select_range_start = 5', 'select_range_end = 25', to create images 5-25 from the list.
select_range_start = 0
select_range_end = 35




#*************************************************
#       This code should not be altered
#*************************************************
#empty list to hold images's of finished craters
image_list = []
totals_list = []


#query CDA for all finished craters
finished = models.CDA.query.filter(or_(models.CDA.vote_result == 'yes',
                                        models.CDA.vote_result == 'no', 
                                        models.CDA.vote_result == 'recenter',
                                        models.CDA.vote_result == 'review',
                                        models.CDA.vote_result == 'unsure'))


print("generating image list")
for i, val in enumerate(finished):
    if not finished[i].image in image_list:
        image_list.append(finished[i].image)
image_len = len(image_list)
i=0
print("evaluating image list")
for image_entry in image_list:
    
    yes = 0
    no = 0
    recenter = 0
    review = 0
    total = 0
    SU = 0
    available = 0
    fin_short = models.CDA.query.filter(and_(models.CDA.image == image_entry, models.CDA.IOU <= .25))
    for fin_entry in fin_short:
        available += 1
        if (fin_entry.vote_result == 'yes'):
            yes += 1
            total += 1
        elif (fin_entry.vote_result == 'no'):
            no += 1
            total += 1
        elif (fin_entry.vote_result == 'recenter'):
            recenter += 1
            total += 1
        elif (fin_entry.vote_result == 'review'):
            review += 1
            total += 1
        if (fin_entry.results_SU_vote >= 1):
            SU +=1

    image_craters = {
        "yes": yes,
        "no": no,
        "recenter": recenter,
        "total": total,
        "image_name": image_entry,
        "available": available,
        "review": review,
        "super_user": SU
    }
    totals_list.append(image_craters)
 
    print("Item {} out of {} finished".format((i+1),image_len))
    i += 1

#sort list in ascending order and print contents
print("Sorting list")
new_list = sorted(totals_list, key=itemgetter('total'), reverse = True) 
for y, val in enumerate(new_list):
    print("List Position: {}, Finished Craters: {}, # Yes: {}, # No: {}, # Re-Center: {}, # Review: {}, #Super_User {} Image Name: {}, Total Craters: {}".format(
                                                                        y,
                                                                        new_list[y]['total'],
                                                                        new_list[y]['yes'],
                                                                        new_list[y]['no'],
                                                                        new_list[y]['recenter'],
                                                                        new_list[y]['review'],
                                                                        new_list[y]['super_user'],
                                                                        new_list[y]['image_name'],
                                                                        new_list[y]['available']
                                                                        ))



#create images
if (create_images == True):
    if ((select_type == 'all') or (select_type == 'individual') or (select_type == 'range')):

        #make image list based on user selections
        num_list = []
        if select_type == 'all':
            num_list = range(0,(len(new_list)-1))

        if select_type == 'individual':
            num_list = select_individual_images

        if select_type == 'range':
            num_list = range(select_range_start, select_range_end)


        for i_num in num_list:    
            
            print("drawing rectangle on {}".format(new_list[i_num]['image_name']))
            rect_short = models.CDA.query.filter(and_(models.CDA.image == new_list[i_num]['image_name'], models.CDA.vote_result != None))
            img_path_name = new_list[i_num]['image_name']
            img_path, img_name = [str(s) for s in img_path_name.split('/')]
            image_to_rect = 'app/static/' + img_path_name
            image_to_write = 'data/images/result_' + img_name
            
            img = cv.imread(image_to_rect)
            
            font = cv.FONT_HERSHEY_COMPLEX_SMALL
            for i, val in enumerate(rect_short):
                if (rect_short[i].vote_result != 'recenter'):
                    x1 = rect_short[i].x1
                    y1 = rect_short[i].y1
                    x2 = rect_short[i].x2
                    y2 = rect_short[i].y2
                else:
                    recenter_vals = models.Vote.query.get(rect_short[i].recenter_id)
                    print('-- recenter query -- ')
                    x1 = recenter_vals.x1_new
                    y1 = recenter_vals.y1_new
                    x2 = recenter_vals.x2_new
                    y2 = recenter_vals.y2_new
                    print("vote: {}, Original: {}, X1: {}".format(recenter_vals.x1_new, rect_short[i].x1,x1))


                no_num = rect_short[i].results_no
                if no_num == None:
                    no_num = 0
                yes_num = rect_short[i].results_yes
                if yes_num == None:
                    yes_num = 0
                count_string = str(yes_num)+':'+str(no_num)+':'+str(rect_short[i].id)
                #no = red
                if rect_short[i].vote_result == 'no':
                    B = 0
                    G = 0
                    R = 255
                #yes = green
                elif rect_short[i].vote_result == 'yes':
                    B = 0
                    G = 255
                    R = 0
                #recenter = blue
                elif rect_short[i].vote_result == 'recenter':
                    B = 255
                    G = 0
                    R = 0
                #unsure = yellow
                elif rect_short[i].vote_result == 'unsure':
                    B = 0
                    G = 255
                    R = 255
                #review = purple
                elif rect_short[i].vote_result == 'review':
                    B = 255
                    G = 0
                    R = 255
                #anything else = black 
                else:
                    B = 0
                    G = 0
                    R = 0
                


                text_yval = y2 + 10
                SU_text_xval = x1 - 8
                if (rect_short[i].results_SU_vote >= 1):
                    cv.putText(img, 'S', (SU_text_xval,text_yval),font,0.7,(0,255,255))
                
                cv.rectangle(img, (x1, y1), (x2, y2), (B,G,R), 2)
                cv.putText(img, count_string, (x1,text_yval),font,0.7,(B,G,R))
                cv.putText(img, img_name, (50,50),font,0.7,(0,255,0))
            cv.imwrite(image_to_write,img)
    else:
        print("Error: Check 'select_type' setting.")

