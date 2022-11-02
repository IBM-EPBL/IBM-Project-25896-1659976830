from flask import Flask,render_template,request,redirect,url_for,session
from datetime import *
from jinja2 import Template
import urllib.robotparser as rb
import dateutil

  
app = Flask(__name__,template_folder="template") 
app.secret_key='a' 

@app.route('/site',methods=['GET', 'POST'])
def site():
    if request.method == 'POST' :
       msg=''
       bot = rb.RobotFileParser()
       x=request.form['website'] 
       if bot.can_fetch('*',x):
          msg="Can access website"
          return render_template("form.html",data=msg)
       else:
          msg="can not access the website"
          return render_template("form.html",data=msg)
       
 
@app.route('/date',methods=['GET', 'POST'])  
def date ():
    if request.method == 'POST' :
        now = datetime.now() # current date and time
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        return render_template("form.html",date=date_time)

@app.route('/',methods=["POST", "GET"])  
def login():   
    if request.method == 'POST' :
        session['username']=request.form['username'] 
        pwd=request.form['password'] 
        return redirect(url_for("success"))  
    return render_template("login.html") 
 
@app.route('/success')  
def success():
    user= session['username']
    msg="Welcome "+user
    return render_template("form.html",msg=msg)
  
if __name__ == '__main__':  
    app.run(debug = True)  