from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.types import PickleType, TypeDecorator, VARCHAR
from sqlalchemy.ext.mutable import Mutable, MutableDict
from sqlalchemy import JSON


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Event(db.Model):
    name = db.Column(db.String(200), primary_key=True, nullable =False)
    init_ticket = db.Column(db.String(200), nullable =False)
    tickets=db.relationship('Tickets', backref='event_ref')
    
class Tickets(db.Model):
    id=db.Column(db.Integer, primary_key=True, nullable =False)
    event_name = db.Column(db.String(200), db.ForeignKey('event.name'))
    redeemed = db.Column(db.Boolean)
    

    
def __repr__(self):
    return '<Event %r>' %self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    events = Event.query.order_by(Event.name).all()
    tickets = Tickets.query.all()
    return render_template('index.html', events=events, tickets=tickets)

@app.route('/addevent/',methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        event_content = request.form['content']
        initial_ticket = request.form['content_ticket']
        new_event = Event(name=event_content, init_ticket = initial_ticket)

        try:
            db.session.add(new_event)
            db.session.commit()
            for x in range(int(initial_ticket)):
                tick = Tickets(event_ref=new_event, redeemed=True)
                db.session.add(tick)
                db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        
        return render_template('addevent.html')

@app.route('/redeem/<id>')
def redeem(id):
    val = id.split("-")
    
    ticket_redeem = Event.query.get_or_404(val[0])
    ticket_redeem.ticket["redeemed"].append(ticket_redeem.ticket["available"][0])
    ticket_redeem.ticket["available"].pop(0)
    print(ticket_redeem.ticket["redeemed"])
    test=Event(name = ticket_redeem.name, init_ticket = ticket_redeem.init_ticket, ticket=ticket_redeem.ticket)
    print(ticket_redeem.ticket)
    try:
        db.session.delete(ticket_redeem)
        db.session.add(test)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem redeeming the ticket'
         

if __name__=="__main__":
    app.run(debug=True)
    
    