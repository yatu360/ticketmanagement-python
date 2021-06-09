from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventdb.db'
db = SQLAlchemy(app)

class Event(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #date_event = db.Column(db.String(200), nullable =False)
    Event_name = db.Column(db.String(200), nullable =False)
    #tickets = db.Column(db.Integer, nullable = False)
    #redeemed = db.Column(db.String(200))
    #description = db.Column(db.String(500))
    
def __repr__(self):
    return '<Event %r>' %self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        event_name = request.form['content_name']
        #event_tickets = request.form['content_ticket']
        new_event = Event(Event_name=event_name)

        try:
            db.session.add(new_event)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        events = Event.query.order_by(Event.date_created).all()
        return render_template('index.html', events=events)

if __name__=="__main__":
    app.run(debug=True)