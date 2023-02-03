from peewee import *

db = SqliteDatabase('test.db')

class User(Model):
    email = TextField(unique=True, null=False)
    password = TextField(null=False)

    class Meta:
        database = db # This model uses the "people.db" database.

class Note(Model):
    user = ForeignKeyField(User, to_field='id')
    name = CharField()
    description = CharField()
    #date = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.



def initialize_db():
    db.connect()
    db.create_tables([Note, User], safe = True)
    #db.drop_tables([Note], safe = True)
    db.close()