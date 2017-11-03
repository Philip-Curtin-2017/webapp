from app import db

#var1 and var2 fields were added early in the project incase extra fields were
#needed for unforseen issues. At present they do not hold any imortant data and can
#be written over or ignored.

class CDA(db.Model):
    __tablename__='CDA_results'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120))
    x1 = db.Column(db.SmallInteger)
    x2 = db.Column(db.SmallInteger)
    y1 = db.Column(db.SmallInteger)
    y2 = db.Column(db.SmallInteger)
    score = db.Column(db.Float)
    GT_conflict = db.Column(db.Boolean)
    votes = db.Column(db.SmallInteger,default=0)
    timestamp = db.Column(db.DateTime)
    IOU = db.Column(db.Float)
    var1 = db.Column(db.String(120))
    var2 = db.Column(db.String(120))
    recenter_id = db.Column(db.Integer, db.ForeignKey('votes.id'), nullable = True)
    vote_result = db.Column(db.String(120))
    results_yes = db.Column(db.SmallInteger)
    results_no = db.Column(db.SmallInteger)
    results_unsure = db.Column(db.SmallInteger)
    results_recenter = db.Column(db.SmallInteger)
    results_SU_vote = db.Column(db.SmallInteger)



    def __repr__(self):
        return '<CDA %r>' % self.id



class GroundTruth(db.Model):
    __tablename__='groundtruths'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120))
    x1 = db.Column(db.SmallInteger)
    x2 = db.Column(db.SmallInteger)
    y1 = db.Column(db.SmallInteger)
    y2 = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<GroundTruth %r>' % self.id


class Vote(db.Model):
    __tablename__='votes'
    id = db.Column(db.Integer, primary_key=True)
    crater_id = db.Column(db.Integer, db.ForeignKey('CDA_results.id'))
    start_timestamp = db.Column(db.DateTime)
    end_timestamp = db.Column(db.DateTime)
    vote_result = db.Column(db.String(20))
    x1_new = db.Column(db.SmallInteger, nullable =True)
    x2_new = db.Column(db.SmallInteger, nullable =True)
    y1_new = db.Column(db.SmallInteger, nullable =True)
    y2_new = db.Column(db.SmallInteger, nullable =True)
    session_data = db.Column(db.String(120))
    var1 = db.Column(db.String(120))
    var2 = db.Column(db.String(120))
    recenter_zscore = db.Column(db.Float)
    vote_type = db.Column(db.String(120))


    def __repr__(self):
        return '<Vote %r>' % self.id


