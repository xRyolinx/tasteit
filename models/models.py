# Tables
class Person(db.Model):
    # Table name
    __tablename__='people'
    
    # Collumns
    id = db.Column(db.Integer,primary_key=True)
    
    username = db.Column(db.TEXT)
    email = db.Column(db.TEXT)
    password = db.Column(db.TEXT)
    pdp = db.Column(db.BYTEA)
    admin = db.Column(db.Integer)
    
    first_name = db.Column(db.TEXT)
    last_name = db.Column(db.TEXT)
    adress = db.Column(db.TEXT)
    phone = db.Column(db.TEXT)
    
    # Initialisate
    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password
