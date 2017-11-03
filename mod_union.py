#!flask/bin/python
from app import db, models
from pprint import pprint



cda_list =[]
gt_list = []
IOU_count = 0


#this function was modeled after the free resouce found at
#https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
def bb_intersection_over_union(cda, GT):
    iou = 0

    # determine the (x, y)-coordinates of the intersection rectangle
    xA = int(max(cda.x1, GT.x1))
    yA = int(max(cda.y1, GT.y1))
    xB = int(min(cda.x2, GT.x2))
    yB = int(min(cda.y2, GT.y2))

   
   # check that the two boxes have overlapping area
    if ((xA <= xB) and (yA <= yB)):
        #check that the boxes are similar sizes
        size_ratio = (cda.x2-cda.x1) / float(GT.x2-GT.x1)
        if ((size_ratio >= 0.25) and (size_ratio <= 4)):
            # compute the area of intersection rectangle
            interArea = (xB - xA + 1) * (yB - yA + 1)
            # compute the area of both the prediction and ground-truth
            # rectangles
            boxAArea = (int(cda.x2) - int(cda.x1) + 1) * (int(cda.y2) - int(cda.y1) + 1)
            boxBArea = (int(GT.x2) - int(GT.x1) + 1) * (int(GT.y2) - int(GT.y1) + 1)

            # compute the intersection over union by taking the intersection
            # area and dividing it by the sum of prediction + ground-truth
            # areas - the interesection area
            iou = interArea / float(boxAArea + boxBArea - interArea)

            #print("IA:{}, A:{}, B:{}".format(interArea, boxAArea, boxBArea))

    
    return iou





cda = models.CDA.query.all()
print("generating CDA image name list")
for n, val in enumerate(cda):
    if not cda[n].image in cda_list:
        cda_list.append(cda[n].image)

print("generating specific query")
for n, val in enumerate(cda_list):
    print("---------------------------------processing image {}.".format(n+1))  

    cda_limited = models.CDA.query.filter_by(image = cda_list[n])
    GT_limited = models.GroundTruth.query.filter_by(image = cda_list[n])

    for x, val in enumerate(cda_limited):
        iou_max = 0.0
        print("processing entry {}, current unions {}.".format(cda_limited[x].id, IOU_count))
        cda_limited[x].IOU = 0.0
        db.session.add(cda_limited[x])
        for y, val in enumerate(GT_limited):
            iou = bb_intersection_over_union(cda_limited[x], GT_limited[y])
            if iou > iou_max:
                iou_max = iou
                IOU_count += 1
                cda_limited[x].IOU = iou
                db.session.add(cda_limited[x])
    db.session.commit()

