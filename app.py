from flask import Flask , render_template , request , redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import random
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flash.db'
db = SQLAlchemy(app)

#class Question(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #question = db.Column(db.String(255))
class User(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        username = db.Column(db.String(200), nullable = False)
        email = db.Column(db.String(200), nullable = False)
        password = db.Column(db.String(8), nullable = False)
        user_decks = relationship('Deck')
        def __repr__(self):
            return '<User %r>' % self.username


class Deck(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        name = db.Column(db.String(200), nullable = False)
        last_reviewed = db.Column(db.DateTime , default = datetime.now())
        deck_score = db.Column(db.Integer, nullable = False)
        cards = relationship('Card' , cascade="all, delete-orphan")
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        deck_user = relationship('User', overlaps="user_decks")
        
'''In SQLAlchemy, the overlaps parameter is used in the definition of a bidirectional relationship between 
two classes to indicate that the relationship on one side overlaps with a relationship on the other side. 
This is typically used when you have multiple relationships between the same two classes.'''

class Card(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)

        front = db.Column(db.String(200), nullable = False)
        back = db.Column(db.String(200), nullable = False)
        content = db.Column(db.Text, nullable=True) 
        card_score = db.Column(db.Integer, nullable = False , default = 2)
        last_reviewed = db.Column(db.DateTime , default = datetime.now())
        deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
        card_deck = relationship('Deck', overlaps="cards" )
    
   
    #lazy='dynamic' means that the data will be loaded as needed
    #backref means that the relationship will be created with the user object

import os

if not os.path.exists("./instance/flash.db"):
    with app.app_context():
            db.create_all()
            Users = User.query.all()
            print(Users)
            if not Users:
                print('No Users')
                U1 = User(username='demo', password='demo', email='demo@demo.com')
                db.session.add(U1)
                D1 = Deck(name = "demo_deck1", last_reviewed = datetime.now(), deck_score = 0, user_id = 1)
                # D2 = Deck(name = "demo_deck2", last_reviewed = datetime.now(), deck_score = 0, user_id = 1)
                # D3 = Deck(name = "demo_deck3", last_reviewed = datetime.now(), deck_score = 0, user_id = 1)
                # D4 = Deck(name = "demo_deck4", last_reviewed = datetime.now(), deck_score = 0, user_id = 1)
                # D5 = Deck(name = "demo_deck5", last_reviewed = datetime.now(), deck_score = 0, user_id = 1)
                C1 = Card(front = "EASY1", back = "EASY1", card_score = 2, last_reviewed = datetime.now(), deck_id = 1)
                C2 = Card(front = "EASY2", back = "EASY2", card_score = 2, last_reviewed = datetime.now(), deck_id = 1)
                C3 = Card(front = "MEDIUM1", back = "MEDIUM1", card_score = 2, last_reviewed = datetime.now(), deck_id = 1)
                C4 = Card(front = "MEDIUM2", back = "MEDIUM2", card_score = 2, last_reviewed = datetime.now(), deck_id = 1)
                C5 = Card(front = "HARD1", back = "HARD1", card_score = 2, last_reviewed = datetime.now(), deck_id = 1)
                C6 = Card(front = "HARD2", back = "HARD2", card_score = 2, last_reviewed = datetime.now(), deck_id = 1)
                db.session.add(D1)
                # db.session.add(D2)
                # db.session.add(D3)
                # db.session.add(D4)
                # db.session.add(D5)
                db.session.add(C1)
                db.session.add(C2)
                db.session.add(C3)
                db.session.add(C3)
                db.session.add(C4)
                db.session.add(C5)
                db.session.add(C6)
                db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic here
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username=username,email=email,password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'There was an issue adding new user'
        # Replace this with your actual signup logic    
    return render_template('signup.html')

@app.route('/login',methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        users=User.query.all()
        for user in users:
            if user.username == username and user.password == password:
                print("inside if condition")
                return redirect(f'/user_dashboard/{user.id}')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/user_dashboard/<int:user_id>',methods =['GET'])
def user_dashboard(user_id):
    msg = request.args.get('msg')
    user = User.query.get_or_404(user_id)
    print(user.user_decks)
    return render_template('user_dashboard.html', user = user, msg = msg)

@app.route('/add_deck/<int:user_id>', methods=['GET', 'POST'])
def add_deck(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        print(request.form)
        print("gokul")
        deck_name = request.form['deck_name']
        deck = Deck(name = deck_name, last_reviewed = datetime.now(), deck_score = 0, user_id = user_id)
        try:
            db.session.add(deck)
            db.session.commit()
            return redirect(f'/user_dashboard/{user_id}')
        except:
            return 'There was an issue adding new deck'
        
    return render_template('add_deck.html', user = user )

@app.route('/update_deck/<int:deck_id>', methods=['GET', 'POST'])
def update_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if request.method == 'POST':
        deck.name = request.form['deck_name']
        deck.last_reviewed = datetime.now()
        try:
            db.session.add(deck)
            db.session.commit()
            return redirect(f'/user_dashboard/{deck.deck_user.id}')
        except:
            return 'There was an issue updating deck'
    return render_template('update_deck.html', deck = deck)

@app.route('/delete_deck/<int:deck_id>' )
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    user_id = deck.deck_user.id
    print(user_id)
    try:
        db.session.delete(deck)
        db.session.commit()
        return redirect(f'/user_dashboard/{deck.deck_user.id}')
    except Exception as e:
        print(e)
        return 'There was an issue deleting deck'

@app.route('/add_card/<int:deck_id>', methods=['GET', 'POST'])
def add_card(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    
    if request.method == 'POST':
        front = request.form['front']
        back = request.form['back']
        print(request.form)
        content = request.form['content']
        print(content)
        card = Card(front=front, back=back,content=content, deck_id=deck.id)
        
        try:
            db.session.add(card)
            db.session.commit()
            return redirect(f'/user_dashboard/{deck.deck_user.id}')
        except:
            return 'There was an issue adding the card'
    
    return render_template('add_card.html', deck=deck)

@app.route('/review_cards/<int:deck_id>', methods=['GET', 'POST'])
def review_cards(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    cards = deck.cards
    #remove the cards that has score as 0.
    
    cards = [card for card in cards if card.card_score != 0]
    cards_left = len(cards)
    print(cards_left)
    random.shuffle(cards)
    if cards:
        # cards[0].content = cards[0].content[10:]
        return render_template('review_cards.html', card=cards[0], cards_left = cards_left)
    else:
        deck.last_reviewed = datetime.now()
        db.session.add(deck)
        db.session.commit()
        return redirect(f'/user_dashboard/{deck.deck_user.id}?msg=No cards to review')
    # Check if the current card is the last card in the deck
    # Get the current card and the next card (if not the last card)
@app.route('/update_score/<int:card_id>',methods=['POST'])
def update_score(card_id):
    #return request.form
    card = Card.query.get_or_404(card_id)
    if request.method == 'POST':
        if card.card_score == 1 and request.form['score'] == '1':
            card.card_score = 0
        else:
            card.card_score = int(request.form['score'])
        try:
            card.last_reviewed = datetime.now()
            db.session.add(card)
            db.session.commit()
            return redirect(f'/review_cards/{card.card_deck.id}')
        except:
            return 'There was an issue updating the score'
    return render_template('update_score.html', card=card)

@app.route('/reset_deck/<int:deck_id>') 
def reset_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    cards = deck.cards
    for card in cards:
        card.card_score = 2
    try:
        db.session.add(deck)
        db.session.commit()
        return redirect(f'/user_dashboard/{deck.deck_user.id}')
    except:
        return 'There was an issue resetting the deck'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50505,debug=True)




