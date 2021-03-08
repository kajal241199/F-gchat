from flask import Flask, render_template, request, session, redirect, url_for, flash
from chat import app
from chat.models import *
from chat.models import *
from chat.forms import *
from sqlalchemy import and_
from flask_login import login_user, current_user,logout_user, login_required
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M")

class ans_id:
    id = 0

a_id = ans_id()


@app.route("/")
def home(id = 1):
    a_id.id = 1
    ans = db.session.query(Ans).filter(Ans.id == "1")
    sub = db.session.query(Sub_ques).filter(Sub_ques.perv_ans_id == 1)
    return render_template("index.html" , init_ans = ans , sub = sub , time = current_time)

@app.route("/get")
def get_bot_response():
    response = ""
    flag = 1
    userText = request.args.get('msg')
           
    sub = db.session.query(Sub_ques).filter(and_(Sub_ques.perv_ans_id == a_id.id , Sub_ques.sub_ques_id == int(userText))).first()
    if(sub):
        a_id.id = sub.next_ans_id
        ans = db.session.query(Ans).filter(Ans.id == sub.next_ans_id).first()
        sub = db.session.query(Sub_ques).filter(Sub_ques.perv_ans_id == a_id.id).all()
        response += ans.ans_desc
        response += "<br>"
        for ques in sub:
            response += "<b>" + str(flag) + " " + ques.sub_ques_desc + "</b><br>"
            flag += 1
            print(response)
        
    else:
        ans = db.session.query(Ans).filter(Ans.id == a_id.id).first()
        response = "<b>Please enter the correct option</b><br> <br>" + ans.ans_desc
        sub = db.session.query(Sub_ques).filter(Sub_ques.perv_ans_id == a_id.id).all()
        response += "<br>"
        for ques in sub:
            response += "<b>" + str(flag) + " " + ques.sub_ques_desc + "</b><br>"
            flag += 1
            print(response)
        
    return response


@app.route("/admin" , methods = ["GET" ,"POST"])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('adminrights'))
    form = AdminLogin()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(id = 1).first()
        if form.email.data == admin.email and form.password.data == admin.password:
            login_user(admin)
            return render_template("adminright.html")
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
   
    return render_template("admin.html" , form = form)

@app.route("/logout" )
def admin_logout():
    logout_user() 
    return redirect(url_for("admin_login"))


@app.route("/adminrights")
@login_required
def adminrights():
    return render_template("adminright.html")


@app.route("/registerques" , methods = ["GET" ,"POST"])
@login_required
def addques():
    form = RegisterQues()
    if form.validate_on_submit():
        sub = Sub_ques(
        sub_ques_id = int(form.sub_ques_id.data),
        perv_ans_id = int(form.perv_ans_id.data),
        next_ans_id = int(form.next_ans_id.data),
        sub_ques_desc = str(form.sub_ques_desc.data))
        db.session.add(sub)
        db.session.commit()
        return redirect(url_for('adminrights'))
    return render_template("registerques.html" , form = form)

@app.route("/registerans" ,methods = ["GET" ,"POST"])
@login_required
def addans():
    form = RegisterAns()
    if form.validate_on_submit():
        ans = Ans(
        ans_desc = form.ans_desc.data)
        db.session.add(ans)
        db.session.commit()  
        return redirect(url_for('adminrights'))
    return render_template("registerans.html" , form = form)

@app.route("/showallquery")
@login_required
def showallquery():
    ans_list = []
    dec_list = ['Answer ID' , 
                'Answer Description' ,
                'Sub ID', 
                'Sub Question Id',
                'Sub Question Description',
                'Next Answer Id',
                'Previous Answer ID']
    for ans, sub in db.session.query(Ans, Sub_ques).filter(Ans.id == Sub_ques.perv_ans_id).all():
        ls = []
        ls.append(ans.id)
        ls.append(ans.ans_desc)
        ls.append(sub.id)
        ls.append(sub.sub_ques_id)
        ls.append(sub.sub_ques_desc)
        ls.append(sub.next_ans_id)
        ls.append(sub.perv_ans_id)
        ans_list.append(ls)
    
    return render_template("showallquery.html" , ls = ans_list, dec_list = dec_list)

@app.route("/updateans/<int:id>" ,methods=['POST' , 'GET'])
@login_required
def updateans(id):
    form = RegisterAns()
    ans = Ans.query.get_or_404(id)
    if form.validate_on_submit():
        ans.ans_desc = form.ans_desc.data
        db.session.commit()
        return redirect(url_for('showallquery'))
    
    elif request.method == 'GET':
        form.ans_desc.data = ans.ans_desc

    return render_template("updateans.html" , form = form)    

@app.route("/updateques/<int:id>" ,  methods=['POST' , 'GET'])
@login_required
def updateques(id):
    form = RegisterQues()
    sub = Sub_ques.query.get_or_404(id)
    if form.validate_on_submit():
        sub.sub_ques_id = form.sub_ques_id.data
        sub.perv_ans_id = form.perv_ans_id.data 
        sub.next_ans_id = form.next_ans_id.data 
        sub.sub_ques_desc =  form.sub_ques_desc.data 
        db.session.commit()
        return redirect(url_for('showallquery'))
    
    elif request.method == 'GET':
        form.sub_ques_id.data = sub.sub_ques_id
        form.perv_ans_id.data = sub.perv_ans_id
        form.next_ans_id.data = sub.next_ans_id
        form.sub_ques_desc.data = sub.sub_ques_desc
        form.submit.data = "Update Question"
    
    return render_template("updateques.html" , form = form)

@app.route("/registerquery" ,methods=['POST' , 'GET'])
def registerquery():
    return render_template("registerquery.html")