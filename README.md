# Latest-news-app
Give latest headlines from BBC news, Tell you about weather of your city and currency converter

## Instructions for local host
* Clone this repo `git clone https://github.com/pawangeek/Latest-news-app.git`
* create virtual environment and install dependencies from `requirements.txt`
* Run app `python app.py`

## Instruction for own herokuapp
* Create account at heroku
* Install Heroku cli and login to it 
* Go to own dashboard in browser `https://dashboard.heroku.com/apps`
* Create new app (top right corner)<p>

* Create .gitgnore in venv (In mycase : sublime) + add __pycache__ and .idea to .gitignore
* Then go to your terminal (In mycase : By pycharm)<p>

* Initialize git repo `git init`
* Type `heroku git:remote -a your_app` , `git add .` follwed by `git commit -am "xyz"`
* Finally push it via `git push heroku master`

Cheers !!
