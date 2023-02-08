# from model import Person
from model import Person, db
import json

with open('region_url.json', 'r', encoding='utf-8')as file:
    region_url_dict = json.load(file)

def check_person(user_id):
    # user_idがデータベースに存在するかを参照する関数
    if Person.query.filter_by(user_id = user_id).first():
        message = 'True'
        return message
    else:
        message = 'False'
        return message

def add_person(user_id, region):
    url = region_url_dict[region]
    with db.session.begin(subtransactions=True):
        person_data = Person(user_id=user_id, region=region, url=url, alarm=False)
        db.session.add(person_data)
    db.session.commit()

def check_region(user_id):
    data = Person.query.filter_by(user_id=user_id).first()
    data = data.region
    return data

def upgrade_region(user_id, update_region):
    Person.query.filter_by(user_id=user_id).update(
        {'region':update_region}
    )
    db.session.commit()

def check_alarm(user_id):
    data = Person.query.filter_by(user_id=user_id).first()
    data = data.alarm
    return data

def true_alarm(user_id):
    Person.query.filter_by(user_id=user_id).update(
        {'alarm':True}
    )
    db.session.commit()

def false_alarm(user_id):
    Person.query.filter_by(user_id=user_id).update(
        {'alarm':False}
    )
    db.session.commit()

def get_alarm_user():
    data = Person.query.filter_by(alarm=True).all()
    return data