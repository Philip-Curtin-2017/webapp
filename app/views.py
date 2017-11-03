from flask import render_template, flash, session, g, request, url_for, redirect
from app import app, db, models
from .models import CDA
from datetime import datetime
from sqlalchemy import desc
import crater_funcs

@app.route('/', methods=['GET', 'POST'])

@app.route('/index', methods=['GET', 'POST'])
def index():

    if request.method == "GET":
        return render_template('index.html',title='Home')

    elif request.method == "POST":
        if request.form['selection']=='Training':
            return redirect(url_for('training_1'))
        elif request.form['selection']=='Start':
            return redirect(url_for('consent'))
        elif request.form['selection']=='Background':
            return redirect(url_for('history'))
        elif request.form['selection']=='Participant_Information':
            return redirect(url_for('legal')) 

@app.route('/legal', methods=['GET', 'POST'])
def legal():

    if request.method == "GET":
        return render_template('legal.html',title='legal')

    elif request.method == "POST":
       return redirect(url_for('training_1'))

@app.route('/consent', methods=['GET', 'POST'])
def consent():

    if request.method == "GET":
        return render_template('consent.html',title='Consent')

    elif request.method == "POST":
        if (request.form['selection']=='Start'): 
            try:
                if (request.form['consent'] == 'Yes'):
                    return redirect(url_for('crater', new_entry_flag = 1))
            except:
                pass
        return redirect(url_for('consent'))


@app.route('/history', methods=['GET', 'POST'])
def history():

    if request.method == "GET":
        return render_template('history.html',title='history')

    elif request.method == "POST":
       return redirect(url_for('training_1'))



@app.route('/crater', methods=['GET', 'POST'])
def crater():
    CF=crater_funcs.craterfunc()

    if request.method == "GET":
        if request.args.get('new_entry_flag') is None:
            new_entry_status = 1
        else:
            new_entry_status = int(request.args.get('new_entry_flag'))
            
        if new_entry_status == 1:
            print new_entry_status
            entries = CF.query_database()
            attributes=CF.get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)

        if new_entry_status == 0:
            print new_entry_status
            tempID = int(request.args.get('numID'))
            entries=models.CDA.query.get(tempID)
            attributes=CF.get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)



    elif request.method == "POST":
        tempID = request.form.get(('numID'), type = int)
        entries=models.CDA.query.get(tempID)

        if request.form['selection']=='Yes':
            CF.update_count("yes", entries)
            entries = CF.query_database()
            attributes = CF.get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)

        elif request.form['selection']=='No':
            CF.update_count("no", entries)
            entries = CF.query_database()
            attributes = CF.get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)

        elif request.form['selection']=='Unsure':
            CF.update_count("unsure", entries)
            entries = CF.query_database()
            attributes = CF.get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)

        elif request.form['selection']=='Re-Center':
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('update_coords',numID=tempID))


@app.route('/update_coords', methods=['GET', 'POST'])
def update_coords():
    CF=crater_funcs.craterfunc()

    if request.method == "GET":
        tempID = int(request.args.get('numID'))
        entries=models.CDA.query.get(tempID)
        attributes=CF.get_attributes(entries)
        return render_template('update_coords.html',title='update_coords',item=entries, attributes = attributes)


    elif request.method == "POST":
        if request.form['recenter_status']=='cancel':
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('crater', new_entry_flag = 0, numID=tempID))

        elif request.form['recenter_status']=='submit':
            relativeX = request.form.get(('relX'), type = int)
            relativeY = request.form.get(('relY'), type = int)
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('update_confirm',numID=tempID, relx = relativeX, rely = relativeY))


@app.route('/update_confirm', methods=['GET', 'POST'])
def update_confirm():
    CF=crater_funcs.craterfunc()


    if request.method == "GET":
        print "update confirm get request"
        tempID = int(request.args.get('numID'))
        relativeX = int(request.args.get('relx'))
        relativeY = int(request.args.get('rely'))
        entries=models.CDA.query.get(tempID)
        attributes=CF.get_new_attributes(entries, relativeX, relativeY)
        return render_template('update_confirm.html',title='update_confirm',item=entries, attributes = attributes)


    elif request.method == "POST":
        if request.form['selection']=='Re-Center':
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('update_coords',numID=tempID))

        elif request.form['selection']=='Confirm':
            tempID = int(request.form.get('numID'))
            x1_new = int(request.form.get('x1'))
            x2_new = int(request.form.get('x2'))
            y1_new = int(request.form.get('y1'))
            y2_new = int(request.form.get('y2'))
            entries=models.CDA.query.get(tempID)
            CF.update_coords(entries, x1_new, x2_new, y1_new, y2_new)
            return redirect(url_for('crater', new_entry_flag = 1))



        elif request.form['selection']=='Cancel':
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('crater', new_entry_flag = 0, numID=tempID))

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == "GET":
        return render_template('review.html', title='review')

    if request.method == "POST":
        if request.form['selection']=='Crater_Lookup':
            return redirect(url_for('crater_lookup'))
        else:
            password = False
            try:
                text = request.form['text']
                if text == "geologyrocks":
                    password = True
            except:
                password = False
            if (password == True):
                return redirect(url_for('super_user_crater', new_entry_flag = 1))
            else:
                return redirect(url_for('index'))


@app.route('/super_user_crater', methods=['GET', 'POST'])
def super_user_crater():
    CF=crater_funcs.craterfunc()

    if request.method == "GET":
        if request.args.get('new_entry_flag') is None:
            new_entry_status = 1
        else:
            new_entry_status = int(request.args.get('new_entry_flag'))
            
        if new_entry_status == 1:
            print new_entry_status
            entries = CF.super_user_query()
            attributes=CF.get_attributes(entries)
            return render_template('super_user_crater.html',title='super_user_crater',item=entries, attributes = attributes)

        if new_entry_status == 0:
            print new_entry_status
            tempID = int(request.args.get('numID'))
            entries=models.CDA.query.get(tempID)
            attributes=CF.get_attributes(entries)
            return render_template('super_user_crater.html',title='super_user_crater',item=entries, attributes = attributes)



    elif request.method == "POST":

        try:
            temp = request.form['selection']
            if ((temp != 'Yes') and (temp != 'No') and (temp != 'Unsure') and (temp != 'Re-Center')):
                return redirect(url_for('super_user_crater', new_entry_flag = 1))
        except:
            return redirect(url_for('super_user_crater', new_entry_flag = 1))
     

        tempID = request.form.get(('numID'), type = int)
        entries=models.CDA.query.get(tempID)

        if request.form['selection']=='Yes':
            CF.super_user_update_entry("yes", entries)
            entries = CF.super_user_query()
            attributes = CF.get_attributes(entries)
            return render_template('super_user_crater.html',title='super_user_crater',item=entries, attributes = attributes)

        elif request.form['selection']=='No':
            CF.super_user_update_entry("no", entries)
            entries = CF.super_user_query()
            attributes = CF.get_attributes(entries)
            return render_template('super_user_crater.html',title='super_user_crater',item=entries, attributes = attributes)

        elif request.form['selection']=='Unsure':
            CF.super_user_update_entry("unsure", entries)
            entries = CF.super_user_query()
            attributes = CF.get_attributes(entries)
            return render_template('super_user_crater.html',title='super_user_crater',item=entries, attributes = attributes)

        elif request.form['selection']=='Re-Center':
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('super_user_update_coords',numID=tempID))

@app.route('/super_user_update_coords', methods=['GET', 'POST'])
def super_user_update_coords():
    CF=crater_funcs.craterfunc()

    if request.method == "GET":
        tempID = int(request.args.get('numID'))
        entries=models.CDA.query.get(tempID)
        attributes=CF.get_attributes(entries)
        return render_template('super_user_update_coords.html',title='super_user_update_coords',item=entries, attributes = attributes)


    elif request.method == "POST":
        if request.form['recenter_status']=='cancel':
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('super_user_crater', new_entry_flag = 0, numID=tempID))

        elif request.form['recenter_status']=='submit':
            relativeX = request.form.get(('relX'), type = int)
            relativeY = request.form.get(('relY'), type = int)
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('super_user_update_confirm',numID=tempID, relx = relativeX, rely = relativeY))


@app.route('/super_user_update_confirm', methods=['GET', 'POST'])
def super_user_update_confirm():
    CF=crater_funcs.craterfunc()


    if request.method == "GET":
        print "update confirm get request"
        tempID = int(request.args.get('numID'))
        relativeX = int(request.args.get('relx'))
        relativeY = int(request.args.get('rely'))
        entries=models.CDA.query.get(tempID)
        attributes=CF.get_new_attributes(entries, relativeX, relativeY)
        return render_template('super_user_update_confirm.html',title='super_user_update_confirm',item=entries, attributes = attributes)


    elif request.method == "POST":
        try:
            temp = request.form['selection']
            if ((temp != 'Confirm') and (temp != 'Re-Center') and (temp != 'Cancel')):
                return redirect(url_for('super_user_crater', new_entry_flag = 1))
        except:
            return redirect(url_for('super_user_crater', new_entry_flag = 1))

        if request.form['selection']=='Re-Center':
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('super_user_update_coords',numID=tempID))

        elif request.form['selection']=='Confirm':
            tempID = int(request.form.get('numID'))
            x1_new = int(request.form.get('x1'))
            x2_new = int(request.form.get('x2'))
            y1_new = int(request.form.get('y1'))
            y2_new = int(request.form.get('y2'))
            entries=models.CDA.query.get(tempID)
            CF.super_user_update_coords(entries, x1_new, x2_new, y1_new, y2_new)
            return redirect(url_for('super_user_crater', new_entry_flag = 1))



        elif request.form['selection']=='Cancel':
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('super_user_crater', new_entry_flag = 0, numID=tempID))


@app.route('/crater_lookup', methods=['GET', 'POST'])
def crater_lookup():
    CF=crater_funcs.craterfunc()
    review_nums = []
    reviews = models.CDA.query.filter(models.CDA.vote_result == 'review').order_by(models.CDA.id)
    for review in reviews:
        review_nums.append(review.id)

    if request.method == "GET":
            entries = CF.super_user_query()
            attributes=CF.get_attributes(entries)
            return render_template('crater_lookup.html',
                                    title='crater_lookup',
                                    item=entries, 
                                    attributes = attributes, 
                                    craters_for_review = review_nums)



    elif request.method == "POST":
        if request.form['selection']=='Review':
            return redirect(url_for('review'))

        else:
            try:
                temp = request.form.get(('craterID'),type = int)
                reviewID = int(temp)
            except:
                reviewID = None

            entries=models.CDA.query.get(reviewID)
            if entries == None:
                entries=CF.super_user_query()
            attributes=CF.get_attributes(entries)
            return render_template('crater_lookup.html',
                                    title='crater_lookup',
                                    item=entries, 
                                    attributes = attributes,
                                    craters_for_review = review_nums)



##### Below are only for training and information pages... 



@app.route('/training_1', methods=['GET', 'POST'])
def training_1():

    if request.method == "GET":
        return render_template('training_1.html',title='training_1')

    elif request.method == "POST":
       return redirect(url_for('training_2'))

@app.route('/training_2', methods=['GET', 'POST'])
def training_2():

    if request.method == "GET":
        return render_template('training_2.html',title='training_2')

    elif request.method == "POST":
       return redirect(url_for('training_3'))

@app.route('/training_3', methods=['GET', 'POST'])
def training_3():

    if request.method == "GET":
        return render_template('training_3.html',title='training_3')

    elif request.method == "POST":
       return redirect(url_for('training_4'))

@app.route('/training_4', methods=['GET', 'POST'])
def training_4():

    if request.method == "GET":
        return render_template('training_4.html',title='training_4')

    elif request.method == "POST":
       return redirect(url_for('training_5'))

@app.route('/training_5', methods=['GET', 'POST'])
def training_5():

    if request.method == "GET":
        return render_template('training_5.html',title='training_5')

    elif request.method == "POST":
       return redirect(url_for('training_6'))


@app.route('/training_6', methods=['GET', 'POST'])
def training_6():

    if request.method == "GET":
        return render_template('training_6.html',title='training_6')

    elif request.method == "POST":
        if request.form['selection']=='Yes':
            return redirect(url_for('training_7'))
        else:
            return render_template('training_6.html',title='training_6')


@app.route('/training_7', methods=['GET', 'POST'])
def training_7():

    if request.method == "GET":
        return render_template('training_7.html',title='training_7')

    elif request.method == "POST":
        if request.form['selection']=='No':
            return redirect(url_for('training_8'))
        else:
            return render_template('training_7.html',title='training_7')

@app.route('/training_8', methods=['GET', 'POST'])
def training_8():

    if request.method == "GET":
        return render_template('training_8.html',title='training_8')

    elif request.method == "POST":
        return redirect(url_for('training_9'))



@app.route('/training_9', methods=['GET', 'POST'])
def training_9():

    if request.method == "GET":
        return render_template('training_9.html',title='training_9')

    elif request.method == "POST":
        return redirect(url_for('training_finished'))


@app.route('/training_finished', methods=['GET', 'POST'])
def training_finished():

    if request.method == "GET":
        return render_template('training_finished.html',title='training_finished')

    elif request.method == "POST":
        if request.form['selection']=='Go_Back':
            return redirect(url_for('training_1'))
        elif request.form['selection']=='Start':
            return redirect(url_for('consent'))
