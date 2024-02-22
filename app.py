from flask import Flask,render_template,request,flash,redirect,url_for
from user import UserOperation
from encryption import Encryption
from validate import myvalidate

app=Flask(__name__)
app.secret_key="sdaskdbasud98ausdkjasbd"

validobj=myvalidate()  #validating object

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/user_login")
def userLogin():
    return render_template("user_login.html")

@app.route("/user_signup",methods=["GET","POST"])
def userSignUp():
    if request.method=='GET':
        return render_template("user_signup.html")
    else:
        fname=request.form["fname"]
        lname=request.form["lname"]
        email=request.form["email"]
        user_name=request.form["user_name"]
        password=request.form["password"]
        # ************** validation ************
        frm=[fname,lname,email,user_name,password]
        if(not validobj.required(frm)):
            flash("Field cannot be empty!")
            return redirect(url_for('userSignUp'))


        # *********Password Encryption*************
        e=Encryption()
        password=e.convert(password)

        # *************** User Opertaions inserting into database**********
        userobj=UserOperation()     #creating a object
        r=userobj.username_check(user_name)
        rc=userobj.email_check(email)

        if(r==0 and rc==0):
            userobj.user_insert(fname,lname,email,user_name,password)
            flash("Successfully registered! Login Now")
            return redirect(url_for('userLogin'))
        else:
            if(rc!=0 and r!=0):
                flash("Email and Username already exists!!")
                return redirect(url_for("userSignUp"))
            elif (rc!=0):
                flash("Email already exists!!")
                return redirect(url_for("userSignUp"))
            elif (r!=0):
                flash("Username already exists!!")
                return redirect(url_for("userSignUp"))
            

        # *****************FLASH MESSAGE ****************
        

if __name__ == ("__main__"):
    app.run(debug=True)