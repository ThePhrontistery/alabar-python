from flask import Flask
from flask_apscheduler import APScheduler

from alabar.models import Topic, db
import datetime

app = Flask(__name__)
app.config['JOBS'] = [
        {
            'id': 'job1',
            'func': 'appbatch:job1',
            'args': (),
            'trigger': 'interval',
            #'trigger': 'cron', 'hour': 12, 'minute': 0, 'second': 0,
            'seconds': 10
            
        }
    ]


app.config['SCHEDULER_API_ENABLED'] = True

def job1():
    # Perform your batch operation here
    print("Job 1 executed")
    current_date = datetime.datetime.now()
    print("current_date ", current_date)
    db.session.execute(db.update(Topic).where(Topic.end_date < current_date)
                              .where(Topic.status == True)
                              .values(status=False,end_date=datetime.datetime.now()))
    
    db.session.commit()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

app.run()
