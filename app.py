from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Event(db.Model):
    name = db.Column(db.String(200), primary_key=True, nullable =False)
    init_ticket = db.Column(db.String(200), nullable =False)
    date = db.Column(db.String(10), nullable=False)
    available = db.Column(db.Integer)
    redeemed_ticket = db.Column(db.Integer)
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


@app.route('/check/', methods=['POST', 'GET'])
def check():
    if request.method == 'POST':
        id = request.form['content']
        ticket = Tickets.query.get_or_404(id)
        if ticket.redeemed == True:
            return 'The ticket has been redeemed'
        else:
            return 'The ticket is ok (available)'
    return render_template('check.html')


@app.route('/addevent/',methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        event_content = request.form['content']
        initial_ticket = request.form['content_ticket']
        event_date = request.form['content_date']
        new_event = Event(name=event_content, init_ticket = initial_ticket, date = event_date, 
                          available = initial_ticket, redeemed_ticket= 0)

        try:
            db.session.add(new_event)
            db.session.commit()
            for x in range(int(initial_ticket)):
                tick = Tickets(event_ref=new_event, redeemed=False)
            db.session.add(tick)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        return render_template('addevent.html')   
    
@app.route('/addticket/<name>')
def addticket(name):
    tick = Tickets(event_name=name, redeemed=False)
    event_info = Event.query.get_or_404(name)
    event_info.available += 1
    try:
        db.session.add(tick)
        db.session.commit()
    except:
        return 'There was an issue adding a ticket'
    return view(name)
 
@app.route('/api/addticket/<name>')
def addticket_api(name):
    tick = Tickets(event_name=name, redeemed=False)
    event_info = Event.query.get_or_404(name)
    event_info.available += 1
    try:
        db.session.add(tick)
        db.session.commit()
    except:
        return 'There was an issue adding a ticket'
    return "200: OK"
 
 
@app.route('/view/<name>')
def view(name):
    
    event_info = Event.query.get_or_404(name)
    return render_template('view.html', total = event_info.available+event_info.redeemed_ticket, title = name, 
                           available = event_info.available, redeemed= event_info.redeemed_ticket)


@app.route('/api/view/<name>')
def view_api(name):
    
    event_info = Event.query.get_or_404(name)
    return {"Event Name": event_info.name, "Total Tickets": event_info.available+event_info.redeemed_ticket, 
            "Available tickets": event_info.available, "Redeemed Tickets": event_info.redeemed_ticket}



@app.route('/reset/<name>')
def reset(name):
    refresh_tickets = Tickets.query.filter(Tickets.event_name==name).all()
    event_info = Event.query.get_or_404(name)
    event_info.available = event_info.init_ticket
    event_info.redeemed_ticket = 0
    try:
        for tickets in refresh_tickets:
            db.session.delete(tickets)
        db.session.commit()
        for x in range(int(event_info.init_ticket)):
            tick = Tickets(event_ref=event_info, redeemed=False)
        db.session.add(tick)
        db.session.commit()
    except:
        return 'There was a problem deleting that task'
    return view(name)


@app.route('/redeemticket/<name>')
def redeemticket(name):
    redeem_tickets = Tickets.query.filter(Tickets.event_name==name).all()
    event_info = Event.query.get_or_404(name)
    for tickets in redeem_tickets:
        if tickets.redeemed==False:
            tickets.redeemed=True
            event_info.available -= 1
            event_info.redeemed_ticket += 1
            tick=Tickets(redeemed=tickets.redeemed)
            try:
                db.session.commit()
                return view(name)
            except:
                return 'There was a problem redeeming a ticket'
    return 'There are no more tickets for this event'
    


@app.route('/redeem/<id>')
def redeem_api(id):
    ticket_redeem = Tickets.query.get_or_404(id)
    event_info = Event.query.get_or_404(ticket_redeem.event_name)
    if ticket_redeem.redeemed==True:
        return '410 GONE'
    ticket_redeem.redeemed = True
    event_info.available -= 1
    event_info.redeemed_ticket += 1
    try:
        db.session.commit()
        return '200 OK'
    except:
        return 'There was a problem redeeming the ticket'
         

if __name__=="__main__":
    app.run(debug=True)
    
    