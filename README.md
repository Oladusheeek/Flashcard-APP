# Flashcard app by Oladusheeek
Original app [Flashcard by Tylerhkmontana](https://github.com/tylerhkmontana/flashcard)

a *full-stack flask applictaion* which can be used as an aid to memorize vocabulary. <br><br>

## Built With
![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![Flask Badge](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff&style=for-the-badge)
![SQLAlchemy Badge](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=fff&style=for-the-badge)

## How to run the program

- Clone the repository.

- Make sure python is installed.<br><br>

### On Windows

run the following code on bash.

python -m venv env

source env/Sripts/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

python app.py

<br>

# Usage

## Login

To log in user need to enter his username in field in the login screen and that's all
![login_screen](https://github.com/Oladusheeek/Flashcard/blob/main/readme_images/login_screen.png?raw=true)

## Create a study set

You can create a study set which contains "Name of the deck" and set of cards.   
Each with fields: "word", "transcription", "translation", "description".    
Fields "transcription" and "description" are optional and new card can be added without them.    

![create_studyset](https://github.com/Oladusheeek/Flashcard/blob/main/readme_images/create_studyset.png?raw=true)

You can change number of words in a study set.

## Study 

User can study a set of words in the same manner as he would study words on index cards.  
To see "backside" of the card user just need to hover cursor over the card.  

![study_screen](https://github.com/Oladusheeek/Flashcard/blob/main/readme_images/study_screen.png?raw=true)

## Test

User can take the test on a study set to see how well he memorized the words.     
User can set a time limit for each question(default - 10s), and when he start the test, words of study set will be shown in random order. 

![test_screen1](https://github.com/Oladusheeek/Flashcard/blob/main/readme_images/test_screen1.png?raw=true)

User can use buttons "skip" and "answer" to accelerate test progress.   
Skipped questions will be marked as wrong answers.  
And "answered" questions will be checked in common manner.  
![test_screen2](https://github.com/Oladusheeek/Flashcard/blob/main/readme_images/test_screen2.png?raw=true)

## Result

After end of the test user can see his results with correct and wrong answers. And overall mark in format of Correct answers/All answers and in percentage.
![test_screen3](https://github.com/Oladusheeek/Flashcard/blob/main/readme_images/test_screen3.png?raw=true)


# What was added by me

First of all I remade GUI and visual appearence to make app more user-friendly and eyesight-friendly too xd.

## Match Test

I added new form of test called - Match Test to bring diverse experience.  
User can pass this test if he clicked on correct pairs of words. User can made his first selection in both column.  
If user chose wrong pair then words which was selected will not be selected anymore and user can make new try.  
If user chose correct pair then selected words disappear from screen.  
After all pairs of words answered user will get a notification with congratulaions and will be backed to main page.  

![match_test](https://github.com/Oladusheeek/Flashcard/blob/main/readme_images/match_test.png?raw=true)

## Edit wordset

I added functionality to edit wordset.

![edit_wordset](https://github.com/Oladusheeek/Flashcard/blob/main/readme_images/edit_screen.png?raw=true)

## Export and Import of wordsets

I added functionality to export and import wordsets.   
User can export wordset with click on button "Export" on defined wordset.  
User can import wordset with selecting "Example_wordset.json" in Import Wordset div and then clicking on button "Confirm".    

Exported file has structure like this:  
{  
    "name": "Abbreviations",  
    "words": [  
        {  
            "name": "ASAP",  
            "transcription": "",  
            "translation": "As soon as possible",  
            "description": ""  
        },  
        {  
            "name": "ETA",  
            "transcription": "",  
            "translation": "Estimated time of arrival",  
            "description": ""  
        },  
        ...]  
}  


# On windows

## I had some troubles with launching this app on my configuration, so i will recommend to first try original instruction at the beginning of README, and then if it didn't work try next:

python -m venv env
source env/Sripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade alembic
pip install --upgrade flask-migrate
flask db init
flask db migrate
flask db upgrade
python app.py
