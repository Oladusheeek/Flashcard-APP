import os
from flask import Flask, session, request, url_for, redirect, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
import json


app = Flask(__name__)
# set app secret key to encrypt session key - value
app.secret_key = 'secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Models

# User model
class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), unique=True,  nullable=False)
    wordsets = db.relationship('Wordset', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.name}, id: {self.id}>"

# Wordset model
class Wordset(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    word = db.relationship('Word', backref='word', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Wordset {self.name}, id: {self.id}>"

# Word model
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    transcription = db.Column(db.String(100), nullable=True)
    translation = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    wordset_id = db.Column(db.String(100), db.ForeignKey('wordset.id'), nullable=False)

    def __repr__(self):
        return f"<Word {self.name}, id: {self.id}"

# Create a database if not exist
db.create_all()

## Functions

# Main Dashboard
@app.route("/")
def main():
    user_id = session.get('user_id')

    if user_id:
        wordsets = Wordset.query.filter_by(user_id=user_id).all()    #if there is no user_session 
        return render_template('dashboard.html', wordsets=wordsets)  #
    else:                                                            # then redirect to login
        return redirect(url_for('login'), code=302) 

# User login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(name=username).first()
        
        if user:
            session['user_id'] = user.id
            session['name'] = user.name
        else:
            user_id = str(uuid.uuid4())
            try:
                new_user = User(id=user_id, name=username)
                db.session.add(new_user)
                db.session.commit()
                session['user_id'] = new_user.id
                session['name'] = new_user.name
            except:
                return "Error: unable to create a user"

        return redirect('/')
    else:
        if session.get('user_id'):
            return redirect(url_for('main'), code=302)
        else:
            return render_template('login.html')

# User log out
@app.route('/logout')
def logout():
    # Get user_id from session
    user_id = session.get('user_id')
    
    # Check existense of user_id in session
    if user_id is None:
        return "Error: No user is logged in"

    # Delete user from session
    session.pop("user_id", None)
    session.pop("name", None)

    # Redirect to main page
    return redirect(url_for('main'))

# User creates a wordset
@app.route('/create_wordset', methods=['POST', 'GET'])
def create_wordset():
    if request.method == 'POST':
        
        # Get data from html form
        name = request.form['name']
        words = request.form.getlist('word')
        transcriptions = request.form.getlist('transcription')
        translations = request.form.getlist('translation')
        descriptions = request.form.getlist('description')

        # Create new wordset
        new_wordset = Wordset(id=str(uuid.uuid4()), user_id=session['user_id'], name=name)
        try:
            db.session.add(new_wordset)
            db.session.commit()
        except Exception as e:
            return f"Error: failed to create wordset: {e}"

        # Add words to wordset
        for index, word in enumerate(words):
            transcription = transcriptions[index] if index < len(transcriptions) else ''
            translation = translations[index] if index < len(translations) else ''
            description = descriptions[index] if index < len(descriptions) else ''
            
            new_word = Word(name=word, transcription=transcription, translation=translation, description=description, wordset_id=new_wordset.id)

            try:
                db.session.add(new_word)
                db.session.commit()
            except Exception as e:
                return f"Error: failed to add word: {e}"
        return redirect(url_for('main'), code=302)
    else:
        return render_template('create_wordset.html')

# User edits wordset
@app.route('/edit_wordset/<wordset_id>', methods=['POST', 'GET'])
def edit_wordset(wordset_id):
    # Getting existing wordset through ID
    wordset = Wordset.query.get(wordset_id)
    if not wordset:
        return f"Error: Wordset with id {wordset_id} not found"
    
    if request.method == 'POST':
        # Updating data of wordset
        wordset.name = request.form['name']

        # Get data about words and number of cards
        num_cards = int(request.form['num_cards'])
        words = request.form.getlist('word')
        transcriptions = request.form.getlist('transcription')
        translations = request.form.getlist('translation')
        descriptions = request.form.getlist('description')

        # Deleting all the words
        existing_words = Word.query.filter_by(wordset_id=wordset_id).all()
        for word in existing_words:
            db.session.delete(word)

        # Adding new words to wordset
        for index in range(num_cards):
            word = words[index] if index < len(words) else ''
            transcription = transcriptions[index] if index < len(transcriptions) else ''
            translation = translations[index] if index < len(translations) else ''
            description = descriptions[index] if index < len(descriptions) else ''
            
            new_word = Word(name=word, transcription=transcription, translation=translation, description=description, wordset_id=wordset.id)
            db.session.add(new_word)

        try:
            db.session.commit()
        except Exception as e:
            return f"Error: failed to update wordset: {e}"

        return redirect(url_for('main'), code=302)
    else:
        # Get current data for displaying on user screen
        words = Word.query.filter_by(wordset_id=wordset_id).all()
        return render_template('edit_wordset.html', wordset=wordset, words=words)

# User deletes a wordset with id
@app.route("/delete_wordset/<id>", methods=['POST', 'GET'])
def delete(id):
    if request.method == 'POST':
        print("Received")
        try:
            wordset_to_delete = Wordset.query.get_or_404(id)
        except:
            return "Error: No user with id: %r" % id
        try:
            db.session.delete(wordset_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return "Error: deleteing wordset"
    else:
        return redirect(url_for('main'))

# User deletes word
@app.route('/delete_word/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    word = Word.query.get(word_id)
    if not word:
        return {"error": "Word not found"}, 404

    try:
        db.session.delete(word)
        db.session.commit()
        return {"success": True}, 200
    except Exception as e:
        return {"error": f"Failed to delete word: {e}"}, 500

# User studies cards
# Just displaying cards all the "logic" in html+css files
@app.route("/study/<id>")
def study(id):
    wordset = Wordset.query.filter_by(id=id).first()
    words = Word.query.with_parent(wordset).all()

    return render_template('study.html', wordset=wordset, words=words)

# User testing knowledge of words
@app.route("/test/<id>")
def test(id):
    wordset = Wordset.query.filter_by(id=id).first()
    words = Word.query.with_parent(wordset).all()

    return render_template('test.html', wordset=wordset, words=words)

# Test Result Page Route
@app.route("/result")
def result():
    return render_template('result.html')

# User testing knowledge of words in "match words" format
@app.route('/match/<wordset_id>')
def matching_test(wordset_id):
    wordset = Wordset.query.get(wordset_id)
    words = Word.query.filter_by(wordset_id=wordset_id).all()
    return render_template('match.html', wordset=wordset, words=words)


# Get the first wordset in the database and can see the words associated with the set
@app.route("/wordset")
def wordset():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    wordsets = Wordset.query.filter_by(user_id=user_id).all()
    return render_template('wordsets.html', wordsets=wordsets)

# User imports file with wordset
@app.route('/import', methods=['POST'])
def import_wordset():
    user_id = session.get('user_id')
    if not user_id:
        return {"error": "User not authenticated"}, 401

    # Checking if file provided
    file = request.files.get('wordset_file')
    if not file:
        return {"error": "No file provided"}, 400

    try:
        # Loading wordset file
        data = json.load(file)

        # Checking for data structure
        if not data or 'name' not in data or 'words' not in data:
            return {"error": "Invalid data format"}, 400

        # Creating new wordset for current user
        new_wordset = Wordset(id=str(uuid.uuid4()), user_id=user_id, name=data['name'])
        db.session.add(new_wordset)
        db.session.commit()

        # Adding words to wordset
        for word_data in data['words']:
            new_word = Word(
                name=word_data['name'],
                transcription=word_data.get('transcription'),
                translation=word_data['translation'],
                description=word_data.get('description'),
                wordset_id=new_wordset.id,
            )
            db.session.add(new_word)

        db.session.commit()
        return redirect(url_for('main'))
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")  # Для отладки
        return {"error": f"Failed to parse JSON file: {e}"}, 400

    except Exception as e:
        return {"error": f"An error occurred: {e}"}, 500

# User exports his wordset
@app.route('/export/<wordset_id>', methods=['GET'])
def export_wordset(wordset_id):
    wordset = Wordset.query.get(wordset_id)
    if not wordset:
        return {"error": "Wordset not found"}, 404

    words = Word.query.filter_by(wordset_id=wordset_id).all()
    wordset_data = {
        "name": wordset.name,
        "words": [
            {
                "name": word.name,
                "transcription": word.transcription,
                "translation": word.translation,
                "description": word.description,
            }
            for word in words
        ]
    }

    formatted_json = json.dumps(wordset_data, indent=4, ensure_ascii=False)
    response = Response(
        formatted_json,
        content_type='application/json; charset=utf-8'
    )
    response.headers['Content-Disposition'] = f'attachment; filename="{wordset.name}.json"'

    # Explicitly set content-length
    #response.headers['Content-Length'] = str(len(formatted_json))
    return response

if __name__ == "__main__":
    # Set environment variables
    os.environ["FLASK_APP"] = "app.py"  
    os.environ["FLASK_ENV"] = "production"  # Export works ONLY in production mode
    # Running flask run
    os.system("flask run")

# Displaying routes
@app.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({"endpoint": rule.endpoint, "methods": list(rule.methods), "url": rule.rule})
    return {"routes": routes}