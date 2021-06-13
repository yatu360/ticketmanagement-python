from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
db = SQLAlchemy(app)


'''
Declaring the Event table
'''
class Event(db.Model):
    name = db.Column(db.String(200), primary_key=True, nullable =False)
    init_ticket = db.Column(db.Integer, nullable =False)
    date = db.Column(db.String(10), nullable=False)
    available = db.Column(db.Integer)
    redeemed_ticket = db.Column(db.Integer)
    tickets=db.relationship('Tickets', backref='event_ref')
    

'''
Declaring the Ticket table
'''   
class Tickets(db.Model):
    id=db.Column(db.Integer, primary_key=True, nullable =False)
    event_name = db.Column(db.String(200), db.ForeignKey('event.name'))
    redeemed = db.Column(db.Boolean)
    

'''
Renders the index page
'''
@app.route('/', methods=['POST', 'GET'])
def index():
    events = Event.query.order_by(Event.name).all()
    tickets = Tickets.query.all()
    return render_template('index.html', events=events, tickets=tickets)



'''
Deletes the database and creates a new one, thereby deleting all the entries.
'''
@app.route('/delete1/')
def delete():
    if os.path.exists("event.db"):
        os.remove("event.db")
        db.create_all()
    else:
        return("The file does not exist")    
    return index()



'''
Deletes the database and creates a new one, thereby deleting all the entries.
'''
@app.route('/api/delete/')
def delete_api():
    if os.path.exists("event.db"):
        os.remove("event.db")
        db.create_all()
    else:
        return("The file does not exist")    
    return "All data deleted"


'''
Receives ticket id from the page’s form and displays ‘The ticket is ok (available)’ if the ticket 
is available or ‘The ticket has been redeemed’ if the ticket is redeemed.
'''
@app.route('/check/', methods=['POST', 'GET'])
def check():
    status = ""
    try:
        if request.method == 'POST':
            id = request.form['content']
            ticket = Tickets.query.get_or_404(id)
            if ticket.redeemed == True:
                status = 'The ticket has been redeemed'
            else:
                status =  'The ticket is ok (available)'
    except:
        status = 'There was an error, please input valid ticket ids only'
    return render_template('check.html', status = status)



'''
This method exposes an endpoint where it takes in the unique ticket id as a parameter and returns 
‘The ticket is ok (available)’ if the ticket is available or ‘The ticket has been redeemed’ if the 
ticket is redeemed.
'''
@app.route('/api/check/<id>', methods=['POST', 'GET'])
def check_api(id):
    try:
        ticket = Tickets.query.get_or_404(id)
        if ticket.redeemed == True:
            return 'The ticket has been redeemed'
        else:
            return 'The ticket is ok (available)'
    except:
        '400: Error, invalid ticket identifier'



'''
Receives event name, date of event and the number of initial tickets from form located in addevent.html page. 
Processes the information by initialising the available and redeemed tickets; available = initial tickets and redeemed tickets = 0. 
Finally processes ticket IDs for N tickets of the event and stores them in the Tickets table; this is done via for-loop.
'''
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



'''
Takes in name as a parameter, then queries to retrieve the event information, using which it adds one ticket to 
the available data of the event. The method also adds one ticket to the ticket table and links it to the event as 
well as assigning it with the next increment of ticket ID.
'''
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



'''
This method exposes an endpoint where it takes in the event name as a parameter and adds a ticket its 
available number of tickets. Returns ‘200: OK’ if it successfully added the ticket.
'''
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
 

'''
Takes in name parameter then queries the name to retrieve the information from the database. 
This information is then past to the view template where the information is displayed to the user.
'''
@app.route('/view/<name>')
def view(name):
    
    event_info = Event.query.get_or_404(name)
    return render_template('view.html', total = event_info.available+event_info.redeemed_ticket, title = name, 
                           available = event_info.available, redeemed= event_info.redeemed_ticket)


'''
This method exposes an endpoint where it takes in the event name as a parameter and returns json serialised container 
with event name, total tickets, available tickets, and redeemed tickets.
'''
@app.route('/api/view/<name>')
def view_api(name):
    
    event_info = Event.query.get_or_404(name)
    return {"Event Name": event_info.name, "Total Tickets": event_info.available+event_info.redeemed_ticket, 
            "Available tickets": event_info.available, "Redeemed Tickets": event_info.redeemed_ticket}



'''
Takes in name as a parameter then queries to retrieve the event information, using which it deletes all 
the tickets and reinitialises the event to its original information.
'''
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


'''
Takes in name as a parameter, then queries to retrieve the event information, using which it sets the first available ticket
of the event to be redeemed. The method also changes the value of the redeemed section of 1 ticket from the Ticket table 
linked to the event to be ‘True’.
'''
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
    return view(name)
    


'''
This method exposes an endpoint where it takes in the ticket id as a parameter and redeems the stated ticket, 
if the ticket redemption is successful returns’200: OK’, else it returns ‘410: GONE’ if the ticket has already been redeemed.
'''
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
    app.run()
    
    