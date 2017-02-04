from flask import Flask, jsonify, render_template, request, abort, make_response
from flask import Response,redirect
from linkedin import linkedin
import requests
import pymongo
from pymongo import MongoClient
import simplejson as json
import mysql.connector

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

global objdata


API_KEY = "78ht9j59rm89g2"
API_SECRET = "qaSwXbaBckI0mbMf"
RETURN_URL = "http://talpa.tech/api"
authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL)


@app.route('/auth',methods=['post'])
def get_auth() :
	return redirect(authentication.authorization_url)

@app.route('/',methods=['GET','POST'])
def get_first():
        return render_template('index.html')

@app.route('/clogin',methods=['POST'])
def get_clogin() :
	con = mysql.connector.connect(user='root',password='toor',host='127.0.0.1',database='login')
	cur = con.cursor()
	username  = request.form['form-username']
        password  = request.form['form-password']
	arg = (username,password)
	query = ("SELECT * FROM  clogin WHERE username=%s AND password=%s")
	cur.execute(query, arg)
	da = cur.fetchall()
	if da :
		print "true"
		return render_template('Candidate.html')
	else :
		print "false"
		return render_template('index.html')
        cur.close()
        con.close()


@app.route('/cologin',methods=['POST'])
def get_cologin() :
        con = mysql.connector.connect(user='root',password='toor',host='127.0.0.1',database='login')
        cur = con.cursor()
        username  = request.form['form-username']
        password  = request.form['form-password']
        arg = (username,password)
        query = ("SELECT * FROM  cologin WHERE username=%s AND password=%s")
        cur.execute(query, arg)
	ba = cur.fetchall()
        if ba :
                print "true"
                return render_template('employerForm.html')
        else :
                print "false"
                return render_template('index.html')
	
        cur.close()
        con.close()

@app.route('/signup',methods=['GET','POST'])
def get_second():
        return render_template('signup.html')


@app.route('/signin',methods=['POST'])
def get_signin() :
        con = mysql.connector.connect(user='root',password='toor',host='127.0.0.1',database='login')
        cur = con.cursor()
        username  = request.form['form-username']
        password  = request.form['form-password']
	email = request.form['form-Email']
	acc = request.form['Accounttype']
        arg = (username,password)
	if acc == 1 :
        	query = ("INSERT INTO  cologin values(%s,%s)")
	else :
		query = ("INSERT INTO  clogin values(%s,%s)")
        cur.execute(query, arg)
	con.commit()
        return render_template('index.html')
        cur.close()
        con.close()


@app.route('/api',methods=['GET','POST'])
def get_code():
        code = request.args.get('code')
	authentication.authorization_code = code
	a = authentication.get_access_token()
	parameters = {"oauth2_access_token": a, "format": "json"}
	response=requests.get("https://api.linkedin.com/v1/people/~:(id,first-name,last-name,headline,picture-url,industry,summary,specialties,positions:(id,title,summary,start-date,end-date,is-current,company:(id,name,type,size,industry,ticker)),educations:(id,school-name,field-of-study,start-date,end-date,degree,activities,notes),associations,interests,num-recommenders,date-of-birth,publications:(id,title,publisher:(name),authors:(id,name),date,url,summary),patents:(id,title,summary,number,status:(id,name),office:(name),inventors:(id,name),date,url),languages:(id,language:(name),proficiency:(level,name)),skills:(id,skill:(name)),certifications:(id,name,authority:(name),number,start-date,end-date),courses:(id,name,number),recommendations-received:(id,recommendation-type,recommendation-text,recommender),honors-awards,three-current-positions,three-past-positions,volunteer)",parameters)
	client = MongoClient('localhost', 27017)
	db = client.recruit
	data=json.loads(response.content)
	data1 = db.mycollection.insert_one(data).inserted_id
	objdata = data1
        print data1
	return render_template('git.html')



@app.route('/git',methods=['GET','POST'])
def get_git() :
	username = request.args.get('gitLoad')
	gparameters = {"client_id":"e0147f212727d665bbb5","client_secret":"18bbd0351a287ba25ad8fa671c72baccb2ed5165"}
	url = "https://api.github.com/users/" + str(username)
	gresponse=requests.get(url,gparameters)
	gdata = json.loads(gresponse.content)
	client = MongoClient('localhost', 27017)
        db = client.recruit
	print objdata
	db.mycollection.update({"_id":objdata},{'$set':gdata})
	result = db.mycollection.find_one({"_id":objdata})
        return result
	

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

