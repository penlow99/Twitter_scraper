from flask import Flask, render_template, url_for, redirect, request
import os 


############################
### Initialize flask app ###
############################
app = Flask(__name__)


##############
### ROUTES ###
##############
#-----------------------------------------------------------------
@app.route('/')
def go_home():
    return redirect('/index')
#-----------------------------------------------------------------
@app.route('/index')
def index():
    return render_template('index.html', title="Twitter Scraper")
#-----------------------------------------------------------------
@app.route('/scrape', methods=['POST'])
def scrape():
    email = request.form['email']
    password = request.form['password']
    search = request.form['search']
    tweet_limit = request.form['tweet_limit']
    sleep_time = request.form['sleep_time']
    return render_template('scrape.html', title="Twitter Scraper", email=email, password=password, search=search, tweet_limit=tweet_limit, sleep_time=sleep_time)
#-----------------------------------------------------------------
## if you don't have a favicon, use this route to get rid of the 404 favicon error
# from flask import send_from_directory
# @app.route('/favicon.ico') 
# def favicon():     
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
#-----------------------------------------------------------------

# app import check
if __name__ == '__main__':
    app.run()  