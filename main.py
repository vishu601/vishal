import time
from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
myapp=Flask(__name__)
myapp.secret_key="super secret key"
# main.py ke top par
import os


DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Is line ko dhyaan se dekho
cn = pymysql.connect(
    host=DB_HOST,
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(DB_PORT) if DB_PORT else 3306, # Port number hamesha integer hona chahiye
    autocommit=True
)

@myapp.route("/home")
def home():
    cn = pymysql.connect(host="localhost", user="vishal_dev", password="", db="demo")
    cur = cn.cursor()
    sql = "select * from questions"
    cur.execute(sql)
    n = cur.rowcount
    msg = ""
    if (n>0):
        records = cur.fetchall()
        return render_template("Home.html", data=records)
    else:
        return render_template("home.html",msg="no data")

@myapp.route("/student_reg",methods=["GET","POST"])
def student_reg():
    if (request.method=="POST"):
        name=request.form["t1"]
        enrollment=request.form["t2"]
        course=request.form["t3"]
        adyear=request.form["t4"]
        address=request.form["t5"]
        contect=request.form["t6"]
        email=request.form["t7"]
        password=request.form["t8"]
        confirmpassword=request.form["t9"]
        usertype="student"
        cn=pymysql.connect(host="localhost",port=3306,user="root",password="",db="demo",autocommit=True)
        cur=cn.cursor()
        p1="insert into studentdata values('"+name+"','"+enrollment+"','"+course+"','"+adyear+"','"+address+"','"+contect+"','"+email+"')"
        p2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
        z1=cur.execute(p1)
        z1=cur.rowcount
        z2=cur.execute(p2)
        z2=cur.rowcount
        usertype="student"
        msg=""
        if(z1==1 and z2==1):
            cur.fetchone()
            msg="student data and login data save"
            return render_template("studentreg.html",vgt=msg)
        elif(z1==1):
            cur.fetchone()
            msg="only studnt data save"
            return render_template("studentreg.html",vgt=msg)
        elif(z2==1):
            cur.fetchone()
            msg="only login data save"
            return render_template("studnetreg.html",vgt=msg)
        else:
            msg="no data save"
    else:
        return render_template("studentreg.html")

@myapp.route("/show_student")
def show_student():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            cn=pymysql.connect(host="localhost",port=3306,user="root",password="",db="demo",autocommit=True)
            cur=cn.cursor()
            sql="select * from studentdata "
            cur.execute(sql)
            n=cur.rowcount
            msg=""
            if(n>0):
                records=cur.fetchall()
                return render_template("showstudent.html",data=records)
            else:
                return render_template("showstudent.html",msg="no data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/edit_student",methods=["GET","POST"])
def edit_student():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            if(request.method=="POST"):
                e1=request.form["P1"]
                cn=pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo",
                             autocommit=True)
                cur=cn.cursor()
                sql="select * from studentdata where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    record=cur.fetchone()
                    return render_template("editstudent.html", data=record)
                else:
                    return render_template("editstudent.html", msg="no data found")
            else:
                return  redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@myapp.route("/edit1_student", methods=["GET","POST"])
def edit1_student():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            if (request.method=="POST"):
                name=request.form["T1"]
                enrollment=request.form["T2"]
                course=request.form["T3"]
                adyear=request.form["T4"]
                address=request.form["T5"]
                contect=request.form["T6"]
                email=request.form["T7"]

                cn=pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo",
                                     autocommit=True)
                cur=cn.cursor()
                sql="update studentdata set name='"+name+"',enrollment='"+enrollment+"',course='"+course+ "',adyear='"+adyear+"',address='"+address+"',contect='"+contect+"'where email='"+email+"'"
                cur.execute(sql)
                n = cur.rowcount
                if(n==1):
                    return render_template("edit1student.html", msg="Data changes are saved successfully")
                else:
                    return render_template("edit1student.html", msg="Unable to saved data")
            else:
                return  redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/delete_student",methods=["GET","POST"])
def delete_student():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            if(request.method=="POST"):
                e1=request.form["H1"]
                cn=pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo",
                             autocommit=True)
                cur = cn.cursor()
                sql = " select * from studentdata where email='"+e1+"'"
                cur.execute(sql)
                n = cur.rowcount
                if (n==1):
                    record = cur.fetchone()
                    return render_template("deletestudent.html", data=record)
                else:
                    return render_template("deletestudent.html", msg="no data delete")
            else:
                return redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@myapp.route("/delete_student1",methods=["GET","POST"])
def delete_student1():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            if(request.method=="POST"):
                email = request.form["T7"]
                cn = pymysql.connect(host="localhost", port=3306, user="root", password="vishal@123", db="demo",
                             autocommit=True)
                cur = cn.cursor()
                p1="delete from studentdata where email='"+email+"'"
                cur.execute(p1)
                n=cur.rowcount
                if(n==1):
                    return render_template("deletestudent1.html",msg="Data deleted successfully")
                else:
                    return render_template("deletestudent1.html",msg="Unable to delete data")
            else:
                return  redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/login",methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        email=request.form["T1"]
        password=request.form["T2"]
        cn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo",
                             autocommit=True)
        cur = cn.cursor()
        sql = "select * from logindata where email='"+email+"' AND password='"+password+"'"
        cur.execute(sql)
        n = cur.rowcount
        if(n==1):
            data=cur.fetchone()
            ut=data[2] #get usertype from index 2
            #create session
            session["usertype"]=ut
            session["email"]=email
            #send to page
            if(ut=="admin"):
                return redirect(url_for("admin_home"))
            elif (ut=="student"):
                return redirect(url_for("student_home"))
            else:
                return render_template("login.html",msg="Contact to amdin")
        else:
            return render_template("login.html",msg="Either email or password is incorrect")
    else:
        return render_template("login.html")

@myapp.route("/logout")
def logout():
    if "email" in session:
        session.pop("email",None)
        session.pop("usertype",None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))
@myapp.route("/auth_error")
def auth_error():
    return render_template("AuthError.html")

@myapp.route("/admin_home")
def admin_home():
    #check session
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            return render_template("AdminHome.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@myapp.route("/student_home")
def student_home():
    # check session
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "student"):
            return render_template("studenthome.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))



@myapp.route('/Admin_reg',methods=["GET","POST"])
def Admin_reg():
    if(request.method=="POST"):
        name=request.form["t1"]
        address=request.form["t2"]
        contect=request.form["t3"]
        email= request.form["t4"]
        password = request.form["t5"]
        usertype="admin"

        cn=pymysql.connect(host="localhost",port=3306,user="root",password="",db="demo",autocommit=True)
        cur=cn.cursor()
        p1="insert into admindata values('"+name+"','"+address+"','"+contect+"','"+email+"','"+password+"')"
        p2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
        cur.execute(p1)
        z1=cur.rowcount
        cur.execute(p2)
        z2=cur.rowcount
        usertype="admin"
        mgs=""

        if (z1==1 and z2==1):
            cur.fetchone()
            msg = "admin data and login data save"
            return render_template("Adminreg.html", vgt=msg)
        elif (z1==1):
            cur.fetchone()
            msg="only admindata save"
            return render_template("Admintreg.html", vgt=msg)
        elif (z2==1):
            cur.fetchone()
            msg="only login data save"
            return render_template("Adminreg.html", vgt=msg)
        else:
            msg="no data save"
    else:
        return render_template("Adminreg.html")

@myapp.route('/Admin_home')
def Admin_home():
    if "email" in session :
        ut=session["usertype"]
        e1=session["email"]
        if (ut=="admin"):
            return render_template("auth_error.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/show_admin")
def show_admin():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            cn=pymysql.connect(host="localhost",port=3306,user="root",password="",db="demo",autocommit=True)
            cur=cn.cursor()
            sql="select * from admindata "
            cur.execute(sql)
            n=cur.rowcount
            msg=""
            if(n>0):
                records=cur.fetchall()
                return render_template("showadmin.html",data=records)
            else:
                return render_template("showadmin.html",msg="no data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/admin_change_pass",methods=["GET","POST"])
def admin_change_pass():
    if("email" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            if(request.method=="POST"):
                oldpassword =request.form["t1"]
                newpassword =request.form["t2"]
                cn=pymysql.connect(host="localhost",port=3306,user="root",password="",db="demo",autocommit=True)
                cur=cn.cursor()
                sql="update logindata set password='"+newpassword+"'where email='"+e1+"'and password='"+oldpassword+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("adminchangepass.html",vgt="passwors changed")
                else:
                    return render_template("adminchangepass.html",vgt="invaild password")
            else:
                return render_template("adminchangepass.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/upload_question",methods=["GET","POST"])
def upload_question():
    if ("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut == "student"):
            if(request.method=="POST"):
                subject=request.form["t1"]
                question=request.form["t2"]
                cn=pymysql.connect(host="localhost",port=3306,user="root",password="",db="demo",autocommit=True)
                cur=cn.cursor()
                dt=str(int(time.time()))
                p1="insert into questions values(0,'"+subject+"','"+question+"',"+dt+",'"+e1+"')"
                z1=cur.execute(p1)
                z1=cur.rowcount
                msg=""
                if(z1==1):
                    cur.fetchone()
                    msg="upload question succsesfull"
                    return render_template("uploadquestion.html",vgt=msg)
                else:
                    msg="upload question unsecessfull"
            else:
                return render_template("uploadquestion.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/show_question")
def show_question():
    if ("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut == "student"):
            cn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo", autocommit=True)
            cur = cn.cursor()
            sql = "select * from questions"
            cur.execute(sql)
            n = cur.rowcount
            msg = ""
            if (n > 0):
                records = cur.fetchall()
                return render_template("showquestion.html", data=records)
            else:
                return render_template("showquestion.html", msg="no data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/edit_question",methods=["GET","POST"])
def edit_question():
    if ("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut == "student"):
            if(request.method=="POST"):
                e1=request.form["H1"]
                cn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo",
                             autocommit=True)
                cur = cn.cursor()
                sql = "select * from questions where qid='"+e1+"'"
                cur.execute(sql)
                n = cur.rowcount
                if (n==1):
                    record = cur.fetchone()
                    return render_template("editquestion.html", data=record)
                else:
                    return render_template("editquestion.html", msg="no data found")
            else:
                return redirect(url_for("show_question"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/edit_question1",methods=["GET","POST"])
def edit_question1():
    if ("usertype" in session):
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "student"):
            if(request.method=="POST"):
                qid=request.form["T1"]
                qsubject=request.form["T2"]
                question=request.form["T3"]
                cn=pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo",
                             autocommit=True)
                cur=cn.cursor()
                p1="update questions set qid='"+qid+"',qsubject='"+qsubject+"',question='"+question+"'  where qid='"+qid+"'"
                cur.execute(p1)
                n=cur.rowcount
                if(n==1):
                    return render_template("editquestion1.html",msg="Data changes are saved successfully")
                else:
                    return render_template("editquestion1.html",msg="Unable to saved data")
            else:
                    return  redirect(url_for("show_question"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))



@myapp.route("/delete_question",methods=["GET","POST"])
def delete_question():
    if ("usertype" in session):
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "student"):
            if(request.method=="POST"):
                e1=request.form["H1"]
                cn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo",
                             autocommit=True)
                cur = cn.cursor()
                sql = " select * from questions where qid='"+e1+"'"
                cur.execute(sql)
                n = cur.rowcount
                if (n==1):
                    record = cur.fetchone()
                    return render_template("deletequestion.html", data=record)
                else:
                    return render_template("deletequestion.html", msg="no data delete")
            else:
                return redirect(url_for("show_question"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/delete_question1",methods=["GET","POST"])
def delete_question1():
    if ("usertype" in session):
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "student"):
            if(request.method=="POST"):
                qid=request.form["T1"]
                qsubject=request.form["T2"]
                question=request.form["T3"]
                cn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo",
                             autocommit=True)
                cur = cn.cursor()
                p1="delete from questions where qid='"+qid+"'"
                cur.execute(p1)
                n=cur.rowcount
                if(n==1):
                    return render_template("deletequestion1.html",msg="Data deleted successfully")
                else:
                    return render_template("deletequestion1.html",msg="Unable to delete data")
            else:
                return  redirect(url_for("show_question"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@myapp.route("/solve_question")
def solve_question():
    if ("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut == "student"):
            cn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo", autocommit=True)
            cur = cn.cursor()
            sql = "select * from questions where qby<>'"+e1+"'"
            cur.execute(sql)
            n = cur.rowcount
            msg = ""
            if (n > 0):
                records = cur.fetchall()
                return render_template("solvequestion.html", data=records)
            else:
                return render_template("solvequestion.html", msg="no data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@myapp.route("/solve_question1",methods=['GET','POST'])
def solve_question1():
    if ("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut == "student"):
            qid=request.form["H1"]
            cn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo", autocommit=True)
            cur = cn.cursor()
            sql = "select * from questions where qid="+str(qid)
            s2="select * from solutions where qid="+str(qid)
            cur.execute(sql)
            n = cur.rowcount
            msg = ""
            if (n > 0):
                records = cur.fetchone()
                cur.execute(s2)
                n=cur.rowcount
                if(n>0):
                    solutions=cur.fetchall()
                    return render_template("solve_question1.html", data=records,ans=solutions)
                else:
                    return render_template("solve_question1.html", data=records)
            else:
                return render_template("solve_question1.html", msg="no data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/solve_question2",methods=['GET','POST'])
def solve_question2():
    if ("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut == "student"):
            qid=request.form["H1"]
            solution=request.form["T1"]
            dt=str(int(time.time()))
            cn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo", autocommit=True)
            cur = cn.cursor()
            sql = "insert into solutions values(0,"+qid+",'"+solution+"','"+dt+"','"+e1+"')"
            cur.execute(sql)
            n = cur.rowcount
            msg = ""
            if (n ==1):
                return render_template("solve_question2.html", msg="Solution uploaded")
            else:
                return render_template("solve_question1.html", msg="Error : Cannot upload solution")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/my_question")
def my_question():
    if ("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut == "student"):
            cn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="demo", autocommit=True)
            cur = cn.cursor()
            sql = "select * from questions where qby='"+e1+"'"
            cur.execute(sql)
            n = cur.rowcount
            msg = ""
            if (n > 0):
                records = cur.fetchall()
                return render_template("myquestion.html", data=records)
            else:
                return render_template("myquestion.html", msg="no data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@myapp.route("/Guest")
def Guest():

        return render_template("Guest.html")




if __name__=="__main__":
                myapp.run(debug=True)
