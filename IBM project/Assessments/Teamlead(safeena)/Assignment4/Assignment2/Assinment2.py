

from flask import Flask,render_template,request,redirect,url_for ,session
import ibm_db
import re
app=Flask(__name__,template_folder='templates',static_folder='static')
app.secret_key='a'
conn=ibm_db.connect("Database=bludb;Hostname=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;Port=32286;Security=SSL;SSLServerCertificate=F:\IBM draft project\DigiCertGlobalRootCA.crt;UID=gqn68734;PWD=IJvrQIkrmldUdQzP",'','')
print("successfully connected")
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=''
    
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        sql='SELECT * FROM Users WHERE username=? AND password=?'
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Logged in']=True
            session['id']=account['username']
            userid=account['USERNAME']
            session['username']=account['USERNAME']
            msg='Logged in successfully'
            return render_template('welcome.html',msg=msg)
        else:
            msg='Incorrect username/password'
    return render_template('login.html',msg=msg)

@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method =='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        phoneno=request.form['phoneno']
        sql='SELECT * FROM users WHERE username=?'
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg="Account already exist!"
        elif not re.matc(r'[^@]+@[^@]+\.[^@]+',email):
            msg="Invalid email address"
        elif not re.match(r'[Aa-Za-z0-9]+',username):
            msg="name must contain character and numbers"
        elif not re.match(r'[0-9]+',phoneno):
            msg="phone no must contain only numbers"
        else:
            insert_sql='INSERT INTO user values(?,?,?)'
            prep_stmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,password)
            ibm_db.bind_param(prep_stmt,3,email)
            ibm_db.execute(prep_stmt)
            msg="You have successfully registered"
            return render_template('login.html',msg=msg)
    elif request.method=="POST":
        msg="Please fill out the form"
    return render_template('registration.html',msg=msg)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')



@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session('username',None)
    return render_template("home.html") 

if __name__=="__main__":
    app.run(debug=True ,host='0.0.0.0')
     
     
           
        
        
        