from db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80))
    title = db.Column(db.String(80))
    text = db.Column(db.String(80))

    def __init__(self, date, title, text):
        self.date=date
        self.title=title
        self.text = text

    def json(self):
        return {"id": self.id, 'date':self.date , 'title':self.title, 'text':self.text}

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).first()#select * from items where name=name limit 1 

    @classmethod    
    def find_by_id(cls, id):        
        return cls.query.get(id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()