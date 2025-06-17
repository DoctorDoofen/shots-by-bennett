from datetime import datetime, timedelta
from app.models import db, User, Appointment, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo appointment
def seed_appointments():
    
    demo_user = User.query.filter_by(username='demo_user').first()
    marnie = User.query.filter_by(username='marnie').first()
    
    
    appointment1 = Appointment(
        title='Dentist Appointment',
        description='Routine dental check-up',
        scheduled_time=datetime.now() + timedelta(days=3),
        user_id=demo_user.id
    )

    appointment2 = Appointment(
        title='Meeting with client',
        description='Discuss project deliverables',
        scheduled_time=datetime.now() + timedelta(days=1),
        user_id=marnie.id
    )

    
    db.session.add(appointment1)
    db.session.add(appointment2)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_appointments():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.appointments RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM appointments"))

    db.session.commit()



