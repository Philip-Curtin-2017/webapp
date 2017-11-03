#!flask/bin/python
from app import db, models
import better_exceptions

#This module is intended to create a dataset for graphing ROC curves
#(Recieiver Operating Charactersitc). The resultant CSV files will be
#saved in the webapp/data/csvs diretory.


#insert values for desired Intersection Over Union percentage. 
#Each value will produce a dataset for graphing an ROC curve.
#each value should be greater than 0 and less than 1.
IOU_threshold_list = [0.5]

#Insert the number of data points you want.
number_data_points = 1000

#Use this variable to consider the evaluated results
#set to True to use the results, set to False to ignore the results
#Additional data will be included in the CSV, but the ROC curve can be generated using
#only the 'False Positive Rate' and 'True Positive Rate' columns
use_evaluated_results = False




#*************************************************
#       This code should not be altered
#************************************************* 

#set extreemely large minimum pixle count so it is immediately replaced
min_pix = 5000
num_small = 0




GT = models.GroundTruth.query.all()
gt_len = len(GT)
print("GT has {} entries").format(gt_len)
cda = models.CDA.query.all()
cda_len = len(cda)
print("CDA has {} entries").format(cda_len)


#TP_original = number of predictions where (IOU >= IOU_threshold) and (score >= confidence)
#TP_evaluated = original + predictions where (IOU < IOU_threshold) and vote result is 'yes' or 'recenter'
def TPR(gt_len, cda, confidence, IOU_threshold, use_results):
    TP_original = 0
    TP_evaluated = 0
    TP = 0
    for n, val in enumerate(cda):
        if (cda[n].IOU >= IOU_threshold):
            if (cda[n].score >= float(confidence)):
                TP_original += 1
        if (cda[n].IOU < IOU_threshold):
            if (cda[n].score >= float(confidence)):
                if ((cda[n].vote_result == 'yes') or (cda[n].vote_result == 'recenter')): 
                    TP_evaluated += 1
        if use_results == True:
            TP = TP_original + TP_evaluated
        else:
            TP = TP_original
    tpr = (float(TP)/float(gt_len))
    return dict(
                tpr = float(tpr),
                tp = int(TP),
                tp_original = int(TP_original),
                tp_evaluated = int(TP_evaluated)
                )

#FP_original = number predictions where (score >= confidence) and (IOU < IOU_threshold) and (crater is not small)
#FP_evaluated = same as original - any craters where (vote result = 'yes' or 'recenter')
#Total predictions = number of predictions at confidence, minus small predictions at confidence
def FPR(cda, confidence, IOU_threshold, use_results):
    FP_original = 0
    FP_evaluated = 0
    FP = 0
    num_small = 0
    predictions = 0
    for n, val in enumerate(cda):
        if (cda[n].score >= confidence):
            predictions += 1
            if (cda[n].var1 == "small"):
                num_small += 1
            if ((cda[n].IOU < IOU_threshold) and (cda[n].var1 != "small")):
                FP_original += 1
                if ((cda[n].vote_result == 'yes') or (cda[n].vote_result == 'recenter')): 
                    FP_evaluated +=1
    pred_m_small = predictions - num_small
    if use_results == True:
        FP = FP_original - FP_evaluated
    else:
        FP = FP_original

    fpr = (float(FP)/float(pred_m_small))
    return dict(
                fpr = float(fpr),
                fp = int(FP),
                pred = int(predictions),
                small = int(num_small),
                fp_original = int(FP_original),
                fp_evaluated = int(FP_evaluated),
                predicted_minus_small = int(pred_m_small))

            



print("Checking for minimum GT size")
for m, val in enumerate(GT):
    pix_x = GT[m].x2 - GT[m].x1
    pix_y = GT[m].y2 - GT[m].y1
    if min_pix > pix_x:
        min_pix = pix_x
        print("minimum pixels is {}, GT record number {}, {}".format(min_pix, GT[m].id, GT[m].image))
    if min_pix > pix_y:
        min_pix = pix_y
        print("minimum pixels is {}, GT record number {}, {}".format(min_pix, GT[m].id, GT[m].image))

print("Checking for small craters")
for n, val in enumerate(cda):
    cda_pix_x = cda[n].x2-cda[n].x1
    cda_pix_y = cda[n].y2-cda[n].y1
    #set votes to a large number to identify small conflicts
    if ((cda_pix_x < min_pix) or (cda_pix_y < min_pix)):
        if cda[n].var1 != "small":
            cda[n].var1 = "small"
            db.session.add(cda[n])
        num_small += 1
print("{} total small craters found.".format(num_small))
db.session.commit()


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step


step_size = 1.0/float(number_data_points)


for IOU_threshold in IOU_threshold_list:
    if use_evaluated_results == True:
        name_string = '_evaluated_'
    else:
        name_string = '_original_'
    IOU_string = str(int(IOU_threshold*100.0))
    file_name_path = 'data/csvs/ROC'+name_string+IOU_string

    f_ROC = open(file_name_path,'w')
    f_ROC.write('Confidence,False Positive Rate,True Positive Rate,')
    f_ROC.write('FPR: False positives,FPR: Predictions minus small craters, FPR: Small crater, FPR: Total craters predicted, FPR: False positives original, FPR: False Positives Evaluated,')
    f_ROC.write('TPR: True Positives,TPR: True Positives Original,TPR: True Positives Evaluated,TPR: Ground Truth Length\n')


    for confidence in my_range(0, 0.99, step_size):
        print('Confidence: {}, {}{}'.format(confidence,name_string,IOU_string))
        tpr = TPR(gt_len, cda, confidence, IOU_threshold, use_evaluated_results)
        fpr = FPR(cda, confidence, IOU_threshold, use_evaluated_results)
        f_ROC.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(confidence,
                                                                        fpr['fpr'],
                                                                        tpr['tpr'],
                                                                        fpr['fp'],
                                                                        fpr['predicted_minus_small'],
                                                                        fpr['small'],
                                                                        fpr['pred'],
                                                                        fpr['fp_original'],
                                                                        fpr['fp_evaluated'],
                                                                        tpr['tp'],
                                                                        tpr['tp_original'],
                                                                        tpr['tp_evaluated'],
                                                                        gt_len))
    f_ROC.close()
            
