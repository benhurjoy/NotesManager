from flask import Flask,render_template,redirect,url_for,request,session,send_file,Response
from config import EMAIL_USER,EMAIL_PASS,SECRET_KEY
from database import find_user,create_table,insert_user,check_password,find_user_email,update_password,create_notes_table,insert_notes,find_notes,deleteNote,find_notes_id,updateNote,create_files_table,insert_files_table,find_file,find_file_id,delete_file_id,db_search,find_user_id
import re
import random as r
import yagmail
import os 
import io
app=Flask(__name__)
app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"]="uploads"
os.makedirs(app.config["UPLOAD_FOLDER"],exist_ok=True)
create_table()
create_notes_table()
create_files_table()
def send_email(to_email,otp):
    yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASS)
    yag.send(
    to=to_email,
    subject="verification otp for notes manager web application",
    contents=f"OTP-{otp} ,for the verification of the email")
@app.route("/")
def home():
    session.clear()
    return render_template("home.html")
@app.route("/register",methods=["GET",'POST'])
def register():
    if  request.method=="POST":
         username=request.form.get("username")
         email=request.form.get("email")
         if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",email):
             message="Invalid email"
             message_type="error"
             return render_template("register.html",message=message,message_type=message_type)
         mail=email
         password=request.form.get("password")
         cpassword=request.form.get("confirm password")
         if password!=cpassword:
              return render_template("register.html",message="passwords not match",message_type="error")
         errors = []
         if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
         if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter.")
         if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter.")
         if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit.")
         if not re.search(r"[@$!%*?&]", password):
            errors.append("Password must contain at least one special character (@, $, !, %, *, ?, &).")

         if errors:
            return render_template("register.html",
                                   message="<br>".join(errors),
                                   message_type="error")
         existing_user=find_user(username)
         existing_email=find_user_email(email)
         if existing_user:
             return render_template("register.html",message="username already taken",message_type="error")
         if existing_email:
             return render_template("register.html",message="email already registered please login",message_type="error")
         gen_otp=r.randrange(1000,9999)
         session["genotp"]=gen_otp
         session["username"]=username
         session["email"]=email
         session["password"]=password
         send_email(email,gen_otp)
         return redirect("/email")
         
    return render_template("register.html")
@app.route("/email", methods=["GET",'POST'])
def email():
    if request.method=="POST":
         otp=request.form.get("otp")
         if int(otp)==int(session["genotp"]):
             insert_user(session["username"],session["password"],session["email"])
             session["id"]=find_user_id(session["username"])
             return render_template("email.html",message="email verified successfully and user registered",message_type="success")
         else:
             return render_template("email.html",message="please enter valid otp",message_type="error")
    return render_template("email.html")
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user=find_user(username)
        if not user:
            return render_template("login.html",message="username does not exist",message_type="error")
        storedPassword=user["PASSWORD"]
        if check_password(storedPassword,password):
            session["username"]=user["USERNAME"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html",message="incorrect password",message_type="error")
            
    return render_template("login.html")
@app.route("/user/dashboard")
def dashboard():
    if "username" not in session:
        return render_template("login.html")
    return  render_template("dashboard.html",message=session["username"])
@app.route("/user/add_note",methods=["GET","POST"])
def add_note():
    if request.method=="POST":
        title=request.form.get("title")
        content=request.form.get("content")
        insert_notes(session["username"],title,content)
        return render_template("addNotes.html",message="Notes successfully Added",message_type="success")
    return render_template("addNotes.html")
@app.route("/user/view_notes")
def view_notes():
    notes=find_notes(session["username"])
    return render_template("viewNotes.html",notes=notes)
@app.route("/user/view_note/<nid>")
def view_note(nid):
    note=find_notes_id(nid)
    return render_template("viewNote.html",note=note)
@app.route("/user/update_note/<nid>",methods=["GET","POST"])
def update_note(nid):
    note=find_notes_id(nid)
    if request.method=="POST":
        title=request.form.get("title")
        content=request.form.get("content")
        updateNote(title,content,nid)
        return render_template("editNotes.html",message="Successfully",message_type="success",nid=nid,note=note)
    return render_template("editNotes.html",nid=nid,note=note)
@app.route("/user/delete_note/<nid>")
def delete_note(nid):
    deleteNote(nid)
    return redirect(url_for("view_notes"))
@app.route("/user/upload_file",methods=["GET",'POST'])
def upload_file():
    if request.method=="POST":
        file=request.files.get("file")
        file_name=file.filename
        file_path=os.path.join(app.config["UPLOAD_FOLDER"],file_name)
        file.save(file_path)
        username=session["username"]
        insert_files_table(username,file_name,file_path)
        return redirect(url_for('view_files'))
    return render_template("uploadFiles.html")
    
@app.route("/user/view_files")
def view_files():
    username=session["username"]
    files=find_file(username)
    return render_template("view_files.html",files=files)
@app.route('/user/view_files/view_file/<fid>')
def view_file(fid):
    file = find_file_id(fid)
    file_path = file['FILE_PATH']
    return send_file(file_path, as_attachment = False)

@app.route('/user/view_files/dowload_file/<fid>')
def download_file(fid):
    file = find_file_id(fid)
    file_path = file['FILE_PATH']
    return send_file(file_path, as_attachment = True)
@app.route('/user/view_files/delete_file/<fid>')
def delete_file(fid):
    file = find_file_id(fid)
    file_path = file['FILE_PATH']
    os.remove(file_path)
    delete_file_id(fid)
    return redirect(url_for('view_files'))

@app.route('/user/search', methods = ['POST', 'GET'])
def search():
    if not session['username']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form.get('query')
        username = session['username']
        notes = db_search(query,username)
        return render_template('search.html', notes = notes)
    return render_template('search.html')
@app.route("/user/export_notes")
def export_notes():
    if not session["username"]:
        return render_template("login.html")
    notes=find_notes(session["username"])
    return render_template("export_notes.html",notes=notes)
@app.route("/user/export_note_txt/<nid>")
def export_note_txt(nid):
    if not session["username"]:
        return render_template("login.html")
    note=find_notes_id(nid)
    buffer = io.StringIO()
    buffer.write(f"{note['NOTES_TITLE']}\n\n{note['CONTENT']}")
    buffer.seek(0)

    return Response(
        buffer.getvalue(),
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment;filename={note['NOTES_TITLE']}.txt"}
    )
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/verify",methods=["POST","GET"])
def verify():
        if request.method=="POST":
         otp=request.form.get("otp")
         print(session["gen_otp"])
         if int(otp)==int(session["gen_otp"]):
             return render_template("changePassword.html")
         else:
             return render_template("femail.html",message="please enter valid otp",message_type="error")
        return render_template("femail.html")

@app.route("/forgot_password",methods=["GET","POST"])
def forgot_password():
     if request.method=="POST":
          femail=request.form.get("email")
          print(femail)
          existing_user=find_user_email(femail)
          if existing_user:
                       gen_otp=r.randrange(1000,9999)
                       session["gen_otp"]=gen_otp
                       session["femail"]=femail
                       send_email(femail,gen_otp)
                       return redirect(url_for("verify"))
          return render_template("forget.html",message="email is not registered please register",message_type="error")
     return render_template("forget.html")
@app.route("/PasswordChange",methods=["GET","POST"])
def PasswordChange():
    if request.method=="POST":
        new_password=request.form.get("new_password")
        cpassword=request.form.get("password")
        if new_password!=cpassword:
            return render_template("ChangePassword.html",message="Passwords does not match",message_type="error")
        print(session["femail"])
        update_password(new_password,session["femail"])
        return render_template("changePassword.html",message="Password updated successfully",message_type="success")
    return render_template("changePassword.html")
app.run(debug=True)