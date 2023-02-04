from peewee import *

db = SqliteDatabase('test.db')

class User(Model):
    email = TextField(unique=True, null=False)
    password = TextField(null=False)

    class Meta:
        database = db 

class Note(Model):
    user = ForeignKeyField(User, to_field='id')
    name = CharField()
    description = CharField()

    class Meta:
        database = db 



def initialize_db():
    db.connect()
    db.create_tables([Note, User], safe = True)
    db.close()