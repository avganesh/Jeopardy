from flask import Flask, render_template, request
from flask_heroku import Heroku
import pandas as pd 
import random
import json

app = Flask(__name__)
heroku = Heroku(app)

#get questions 
q_df = pd.read_json('static/JEOPARDY_QUESTIONS1.json')
q_df['value'] = q_df['value'].str.replace('$', '')
q_df['value'] = q_df['value'].str.replace(',', '')
q_df.dropna(inplace=True)
#q_df['value'] = q_df['value'].astype(int)
#print(q_df.head())
#print(q_df.shape)
#print(q_df[q_df.isnull().any(axis=1)])

def getquestion():
    num = random.randrange(1,216929) 
    return q_df.iloc[num] 

# Set "homepage" to index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    qs = getquestion()
    message = "Thanks for playing, enter your answer and submit."
    return render_template('index.html', message=message, score=0, category=qs['category'], value=qs['value'], clue=qs['question'], correctAnswer=qs['answer'])

@app.route('/getnewquestion', methods=['GET', 'POST'])
def getnewquestion():
    if request.method=='POST':
        qs = getquestion()
    return json.dumps([qs['category'], qs['value'], qs['question'], qs['answer']])

if __name__ == '__main__':
    app.debug = True
    app.run()

