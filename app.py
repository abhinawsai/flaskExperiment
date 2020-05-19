from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__) #creating an app which serves your website using Flask
app.secret_key = '121dsdsdw7dsd2dsxaxsd2'  #Random key so that no one can listen on the connections when making flash messages

@app.route('/')  #creating a routing for default/home page
def home():
    return render_template('home.html', codes=session.keys())   #added an arg codes to show recorded session

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():    #name of the function and name of the route do not have to match
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):   #check if the file exists
            with open('urls.json') as urls_file:   #open the file as urls_file
                urls = json.load(urls_file)      #load the file content to urls

        if request.form['code'] in urls.keys():   #if the short name exists
            flash('That short name has already been taken. Please select another name')
            return redirect(url_for('home'))    #retun to home

        if 'url' in request.form.keys():        #request.form is a dict. All the request functions create dict of the inputs provided.(I guess)
            urls[request.form['code']] = {'url':request.form['url']} #add the short name and the url to the JSON dictionary
        else:
            f = request.files['file']                      #get the file that was uploaded
            full_name = request.form['code'] + secure_filename(f.filename)  #create a unique name for the file
            f.save(r'C:\Users\abhin\Desktop\url-shortener\static\user_files\.' + full_name)  #save the file to a directory
            urls[request.form['code']] = {'file':full_name}   #add the short name and the filename to the JSON dict

        with open('urls.json', 'w') as url_file:            #open the file as urls_file
            json.dump(urls, url_file)                     #append/dump/add updated dict to file
            session[request.form['code']] = True           #recording the code inputs to the session. Session is stored as a dict as well.
        return render_template('your_url.html', yourCode=request.form['code'])
    else:
        return redirect(url_for('home'))

#inside of our route, we can use something called a variable route to say, hey,
#look for a string and then whatever that string is it can be passed into the function and
#then used to determine what to give back to the user.
@app.route('/<string:code>') #look for after the first slash on the website, any sort of string and put it in a variable called code.
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + '.' + urls[code]['file']))
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys())) #we just need to return back those session keys in a list. And make sure that it's in the JSON format.
