from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.password}')"

class Data(db.Model):
    primarykey = db.Column(db.Integer,primary_key = True,autoincrement = True)
    id = db.Column(db.Integer)
    time = db.Column(db.Date,nullable = False)
    machine = db.Column(db.String(255),nullable = False)
    component = db.Column(db.String(255),nullable = False)
    parameter = db.Column(db.String(255),nullable = False)
    value = db.Column(db.Numeric(10,2),nullable = False)
    

    def __repr__(self):
        return f"Data('{self.id}', '{self.time}', '{self.machine}','{self.component}','{self.parameter}','{self.value}')"