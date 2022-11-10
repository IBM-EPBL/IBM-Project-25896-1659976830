from flask import Flask,render_template,request,redirect,url_for,session
import re
app=Flask(__name__,template_folder="template")
app.secret_key='a'

@app.route('/register',methods=['GET','POST'])
def register():
    msg = ''
    
    if request.method =='POST' :
        form_data = request.form.to_dict()
        username=form_data['username']
        email=form_data['email']
        #password=request.form['password']
        phoneno=form_data['phoneno']
     
        
        if re.match(r'[^@]+@[^@]+\.[^@]+',email):
           msg="Invalid email address"
        elif not re.match(r'[^A-Za-z0-9]+',username):
            msg="name must contain character and numbers"
        elif not re.match(r'[0-9]+',phoneno):
           msg="phoneno must contain only numbers"
        else:
           return render_template("data.html",form_data=form_data)
    elif request.method=="POST":
        msg="Please fill out the form"
    return render_template("registration.html",msg=msg)

    
if __name__=="__main__":
    app.run(debug=True)