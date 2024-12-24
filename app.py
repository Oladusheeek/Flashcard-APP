import os
from flask import Flask, session, request, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid

app = Flask(__name__)
# set app secret key to encrypt session key - value
app.secret_key = 'secret'

# local db connection
# if os.environ['ENV'] == 'dev':
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
# else: 
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u563uq13927pv8:p3a1695dab31bf5214b4ef8a5d0b8bc1c35515278df177964bee0bc0969a18eb6@ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d4nven4jtj5jc5'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

# Main Dashboard
@app.route("/")
def main():
    user_id = session.get('user_id')

    if user_id:
        wordsets = Wordset.query.filter_by(user_id=user_id).all()
        return render_template('dashboard.html', wordsets=wordsets)
    else:
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
    # Получаем user_id из сессии
    user_id = session.get('user_id')
    
    # Проверяем, существует ли user_id в сессии
    if user_id is None:
        return "Error: No user is logged in"

    # Удаляем пользователя из сессии
    session.pop("user_id", None)
    session.pop("name", None)

    # Перенаправляем на главную страницу
    return redirect(url_for('main'))

# User creates a wordset
@app.route('/create_wordset', methods=['POST', 'GET'])
def create_wordset():
    if request.method == 'POST':
        
        # Получение данных из формы
        name = request.form['name']
        words = request.form.getlist('word')
        transcriptions = request.form.getlist('transcription')
        translations = request.form.getlist('translation')
        descriptions = request.form.getlist('description')

        # Создание нового wordset
        new_wordset = Wordset(id=str(uuid.uuid4()), user_id=session['user_id'], name=name)
        try:
            db.session.add(new_wordset)
            db.session.commit()
        except Exception as e:
            return f"Error: failed to create wordset: {e}"

        # Добавление слов в wordset
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


@app.route('/edit_wordset/<wordset_id>', methods=['POST', 'GET'])
def edit_wordset(wordset_id):
    # Получение существующей колоды по ID
    wordset = Wordset.query.get(wordset_id)
    if not wordset:
        return f"Error: Wordset with id {wordset_id} not found"
    
    if request.method == 'POST':
        # Обновление данных колоды
        wordset.name = request.form['name']

        # Получение данных о словах и количестве карточек
        num_cards = int(request.form['num_cards'])
        words = request.form.getlist('word')
        transcriptions = request.form.getlist('transcription')
        translations = request.form.getlist('translation')
        descriptions = request.form.getlist('description')

        # Удаление всех существующих слов в колоде
        existing_words = Word.query.filter_by(wordset_id=wordset_id).all()
        for word in existing_words:
            db.session.delete(word)

        # Добавление обновленных слов в колоду, с учетом количества карточек
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
        # Получение текущих данных колоды и слов для отображения в форме редактирования
        words = Word.query.filter_by(wordset_id=wordset_id).all()
        return render_template('edit_wordset.html', wordset=wordset, words=words)

@app.route("/study/<id>")
def study(id):
    wordset = Wordset.query.filter_by(id=id).first()
    words = Word.query.with_parent(wordset).all()

    return render_template('study.html', wordset=wordset, words=words)

@app.route("/test/<id>")
def test(id):
    wordset = Wordset.query.filter_by(id=id).first()
    words = Word.query.with_parent(wordset).all()

    return render_template('test.html', wordset=wordset, words=words)

@app.route('/match/<wordset_id>')
def matching_test(wordset_id):
    wordset = Wordset.query.get(wordset_id)
    words = Word.query.filter_by(wordset_id=wordset_id).all()
    return render_template('match.html', wordset=wordset, words=words)

#if __name__ == '__main__':
#    app.run(debug=True)

############################### this is where you should pick it up from ##############################

# Delete a wordset with id
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

# Wordset helper functions
# get the first wordset in the database and can see the words associated with the set
@app.route("/wordset")
def wordset():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    wordsets = Wordset.query.filter_by(user_id=user_id).all()
    return render_template('wordsets.html', wordsets=wordsets)

# Test Result Page Route
@app.route("/result")
def result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)



import json
from flask import request, session, redirect, url_for

@app.route('/import', methods=['POST'])
def import_wordset():
    user_id = session.get('user_id')
    if not user_id:
        return {"error": "User not authenticated"}, 401

    # Проверка наличия файла
    file = request.files.get('wordset_file')
    if not file:
        return {"error": "No file provided"}, 400

    try:
        # Загрузка и декодирование JSON-файла
        data = json.load(file)

        # Проверка структуры данных
        if not data or 'name' not in data or 'words' not in data:
            return {"error": "Invalid data format"}, 400

        # Создать новый Wordset для текущего пользователя
        new_wordset = Wordset(id=str(uuid.uuid4()), user_id=user_id, name=data['name'])
        db.session.add(new_wordset)
        db.session.commit()

        # Добавить слова в Wordset
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
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON file"}, 400
    except Exception as e:
        return {"error": f"An error occurred: {e}"}, 500


@app.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({"endpoint": rule.endpoint, "methods": list(rule.methods), "url": rule.rule})
    return {"routes": routes}


import json
from flask import Response

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

    # Генерация форматированного JSON
    formatted_json = json.dumps(wordset_data, indent=4, ensure_ascii=False)
    response = Response(formatted_json, content_type='application/json')
    response.headers['Content-Disposition'] = f'attachment; filename={wordset.name}.json'

    return response
