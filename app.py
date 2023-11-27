from flask import Flask,render_template,url_for,redirect,request,flash,session
from flask_mysqldb import MySQL
import re



app=Flask(__name__)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="Bala2905"
app.config["MYSQL_DB"]="crud"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

@app.route('/') 
@app.route('/login',methods=['POST','GET'])
def login():

    if request.method=='POST' and 'email' in request.form and 'password' in request.form:
        email=request.form['email']
        password=request.form["password"]
        con=mysql.connection.cursor()
        con.execute("select * from reg where email=%s and password=%s",[email,password])
        data=con.fetchone()
        if data:
            session['logged_in']=True
            flash('Login Successfully','success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect email/password','danger')
    return render_template("login.html")
  
  
#Registration  
@app.route('/reg',methods=['POST','GET'])
def reg():
    if request.method=='POST' and 'uname' in request.form and 'email' in request.form and 'password' in request.form: 
        uname=request.form["uname"]
        email=request.form["email"]
        password=request.form["password"]
        cun=mysql.connection.cursor()
        cun.execute("SELECT * FROM reg WHERE uname LIKE %s", [uname])
        acc= cun.fetchone()
        SpecialSym =['$', '@', '#', '%']
        if acc:
            flash("Account already exists!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', uname):
            flash("Username must contain only characters and numbers", "danger")
        elif len(password) < 6:
            flash('Password should be at least 6 Characters',"danger")
        elif not any(char.isupper() for char in password):
            flash('Password should have at least one uppercase letter',"danger")
        elif not any(char.islower() for char in password):
            flash('Password should have at least one lowercase letter',"danger")
        elif not any(char.isdigit() for char in password):
            flash('Password should have at least one numeral','danger')
        elif not any(char in SpecialSym for char in password):
            flash('Password should have at least one of the symbols $@#%',"danger")
        else:
            cun.execute("INSERT INTO reg (uname, email, password) VALUES (%s, %s, %s)", [uname,email,password])
            mysql.connection.commit()
            cun.close()
            flash('Registration Successful. Login Here...','success')
            return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/home")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM users"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)

@app.route("/add",methods=['GET','POST'])
def add():
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con=mysql.connection.cursor()
        sql="insert into users(NAME,CITY,AGE) value(%s,%s,%s)"
        con.execute(sql,[name,city,age])
        mysql.connection.commit()
        con.close()
        flash('Employees Details Added','success')
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/edit/<string:id>",methods=['GET','POST'])
def edit(id):
    con=mysql.connection.cursor()

    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con=mysql.connection.cursor()
        sql="update users set NAME=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql,[name,city,age,id])
        mysql.connection.commit()
        con.close()
        flash('Employees Details Updated','success')
        return redirect(url_for("home"))
        con=mysql.connection.cursor()



    sql="select * from users where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("edit.html",datas=res)

@app.route("/delete/<string:id>",methods=['GET','POST'])
def delete(id):
    con=mysql.connection.cursor()
    sql="delete from users where ID=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    flash('Employees Details Deleted','success')
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session['logged_in']=False

    flash('You are now logged out','success')
    return redirect(url_for('login'))



if(__name__=='__main__'):
    app.secret_key="abc"
    app.run( debug=True)
