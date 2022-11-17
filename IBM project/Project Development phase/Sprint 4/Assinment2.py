from flask import Flask,render_template,request,redirect,url_for ,session
import ibm_db
import re
import os
import math
import random
import smtplib
import requests
import json
app=Flask(__name__,template_folder='templates',static_folder='static')
app.secret_key='a'
conn = ibm_db.connect("Database=bludb;Hostname=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;Port=32286;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=gqn68734;PWD=IJvrQIkrmldUdQzP",'','')
print("successfully connected")
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=''
    
    if request.method=='POST':
        username=request.form.get('username',False)
        password=request.form.get('password',False)
        sql='SELECT * FROM USER WHERE username=? AND password=?'
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Logged in']=True
            session['id']=account['USERNAME']
            userid=account['USERNAME']
            session['username']=account['USERNAME']
            msg='Logged in successfully'
            return redirect(url_for('dashboard'))
        else:
            msg='Incorrect username/password'
    return render_template('login.html',msg=msg)

@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method =='POST':
        username=request.form.get('username',False)
        email=request.form.get('email',False)
        password=request.form.get('password',False)
        Firstname=request.form.get('firstname',False)
        lastname=request.form.get('lastname',False)
        #phoneno=request.form['phoneno']
        sql='SELECT * FROM USER WHERE username=?'
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        #ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        session['mail']=email
        print(account)
        if account:
            msg="Account already exist!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg="Invalid email address"
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg="name must contain character and numbers"
       
        else:
            insert_sql='INSERT INTO USER values(?,?,?,?,?)'
            prep_stmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.bind_param(prep_stmt,4,Firstname)
            ibm_db.bind_param(prep_stmt,5,lastname)
            ibm_db.execute(prep_stmt)
            msg="You have successfully registered"
            return render_template('register.html',msg=msg)
    elif request.method=="POST":
        msg="Please fill out the form"
    return render_template('register.html',msg=msg)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/verify')
def verify():
        email=session['mail']
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        password="nsgeuedwbzptosyp"
        server.login("active.1468@gmail.com",password)
        otp=''.join([str(random.randint(0,9))for i in range(4)])
        msg=' YOUR OTP IS'+str(otp)
        server.sendmail("active.1468@gmail.com",email,msg)
        server.quit()
        if request.method=='POST':
            verify=request.method['code']
            if verify==otp:
                return render_template('login.html')
        return render_template('verify.html')
    
@app.route('/frgpwd', methods=['GET','POST'])
def frgpwd():
    msg =" "
    print(request.form)
    username1=request.form.get("uname", False)
    oldpassword=request.form.get("oldpassword", False)
    newpassword=request.form.get("newpassword", False)
    sql='SELECT * FROM USER WHERE username=?'
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,username1)
    #ibm_db.bind_param(stmt,2,password)
    ibm_db.execute(stmt)
    account=ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        chgpwd_sql='UPDATE USER SET password = ? WHERE username = ?'
        prep_stmt=ibm_db.prepare(conn, chgpwd_sql)
        ibm_db.bind_param(prep_stmt,1,newpassword)
        ibm_db.bind_param(prep_stmt,2,username1)
        ibm_db.execute(prep_stmt)
        msg="You have successfully changed password"
        return render_template('forgot password.html',msg=msg)
    return render_template('forgot password.html',msg=msg)

url = "https://low-carb-recipes.p.rapidapi.com"

headers = {
  "x-rapidapi-key": "ad933ea36amsh6b0a83e514b1a58p14bc9ejsne745a5851a1b",
  "x-rapidapi-host":  "low-carb-recipes.p.rapidapi.com"
  }

searchForRecipes = "/search"
getRecipe="/recipes/"
getImage="/images/"
getRandomRecipe="/random"

@app.route('/dash')
def dashboard():
    return render_template('dash.html')

@app.route('/dash/viewprofile')
def viewprofile():
    username=session['id']
    sql='SELECT * FROM USER_DETAILS WHERE name=?'
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,username)
    ibm_db.execute(stmt)
    account=ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        return  render_template('viewprofile.html',account=account)
    else:
        return render_template('peronal info.html')
        

@app.route('/personinfo',methods=['GET','POST'])
def per_info():
    msg=''
    if request.method =='POST':
        Name=request.form.get('name',False)
        gender=request.form.get('gender',False)
        tar_weight=request.form.get('Target Weight',False)
        Age=request.form.get('Age',False)
        Height=request.form.get('Height',False)
        Weight=request.form.get('Weight',False)
        health=request.form.get('Health',False)
        location=request.form.get('Location',False)
        phoneno=request.form.get('Phone Number',False)

        insert_sql='INSERT INTO USER_DETAILS values(?,?,?,?,?,?,?,?,?)'
        prep_stmt=ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt,1,Name)
        ibm_db.bind_param(prep_stmt,2,gender)
        ibm_db.bind_param(prep_stmt,3,Age)
        ibm_db.bind_param(prep_stmt,4,Height)
        ibm_db.bind_param(prep_stmt,5,Weight)
        ibm_db.bind_param(prep_stmt,6,tar_weight)
        ibm_db.bind_param(prep_stmt,7,health)
        ibm_db.bind_param(prep_stmt,8,location)
        ibm_db.bind_param(prep_stmt,9,phoneno)
        ibm_db.execute(prep_stmt)
        msg="Your details are successfully saved"
        return redirect(url_for('viewprofile',msg=msg))
    else:
        msg="Please fill out the form"
    return render_template('peronal info.html',msg=msg)
    

@app.route('/feedback',methods=['GET','POST'])
def feedback():
    msg=''
    if request.method =='POST':
        Name=request.form['name']
        email=request.form['email']
        Feedback=request.form['feedback']
        sql='SELECT * FROM USER WHERE username=?'
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,Name)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            insert_sql='INSERT INTO FEEDBACK values(?,?,?)'
            prep_stmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt,1,Name)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,Feedback)
            ibm_db.execute(prep_stmt)
            msg="Your Feedback has been stored"
            return render_template('ratings.html',msg=msg)
    elif request.method=="POST":
        msg="Please fill out the form"
    return render_template('ratings.html',msg=msg)

@app.route('/dash/view recipe')
def search_page():
  #session ['item']=request.form.get("Ingridients", False)
  return render_template('search.html')
@app.route('/recipes')
def get_recipes():
  #food=session['item']
  if (str(request.args['ingridients']).strip() != ""):
      print(request.args['ingridients'])
      # If there is a list of ingridients -> list
      querystring = {"name":request.args['ingridients'],"tags":request.args['tag'],"includeIngredients":request.args['included'],"excludeIngredients":request.args['excluded'],"maxPrepareTime":"30","maxCookTime":"20","maxCalories":"500","maxNetCarbs":"5","maxSugar":"3","maxAddedSugar":"0","limit":"10"}
      response = requests.request("GET", url + searchForRecipes, headers=headers, params=querystring)
      data=response.json()
      return render_template('recipes.html', recipes=data)
  else:
      # Random recipes
      response = requests.request("GET", url+ getRandomRecipe  , headers=headers)
      data=response.json()
      return render_template('recipes.html', recipes=data)
    
@app.route('/recipe')
def get_recipe():
  recipe_id = request.args['id']
  recipe_info_endpoint = "/recipes/{0}".format(recipe_id)
  print(recipe_info_endpoint)
  recipe_info = requests.request("GET", url + recipe_info_endpoint, headers=headers)
  data=recipe_info.json()
  return render_template('recipe.html', recipe=data)

@app.route('/food', methods=['POST','GET'])
def get_nutri():
    msg=''
    url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"

    headers = {
	"X-RapidAPI-Key": "ad933ea36amsh6b0a83e514b1a58p14bc9ejsne745a5851a1b",
	"X-RapidAPI-Host": "nutrition-by-api-ninjas.p.rapidapi.com"
    }
    if  request.method =='POST':
        food=request.form.get('food')
        if (str(food).strip() != ""):
      
            querystring = {"query":food}
            response = requests.request("GET", url, headers=headers, params=querystring)
            data=response.json()
        #data=json.load(response)
        #datas=data.json()
            print(data)
            return render_template("foodanalyzer.html", result=data)
    return render_template("foodanalyzer.html")


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    return render_template("index.html") 

if __name__=="__main__":
    app.run(debug=True ,host='0.0.0.0',use_reloader=False)
     
     
           
        
        
        