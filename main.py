# main.py
import os
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from camera import VideoCamera
from camera2 import VideoCamera2
import cv2
import csv
from flask_mail import Mail, Message
from flask import send_file
import numpy as np
import shutil
import datetime
import time
import PIL.Image
from PIL import Image
import imagehash
import mysql.connector
from werkzeug.utils import secure_filename

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="face_examhall"

)
app = Flask(__name__)
app.secret_key = 'abcdef'

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
##email
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "rnd1024.64@gmail.com",
    "MAIL_PASSWORD": "kazxlklvfrvgncse"
}

app.config.update(mail_settings)
mail = Mail(app)
#######


@app.route('/')
def index():
    ff=open("det.txt","w")
    ff.write("1")
    ff.close()

    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()

    ff11=open("img.txt","w")
    ff11.write("1")
    ff11.close()

    ff=open("person.txt","w")
    ff.write("")
    ff.close()
    return render_template('web/index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM fe_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            #session['loggedin'] = True
            #session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('admin'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('web/login.html',msg=msg)

@app.route('/login_hod', methods=['GET', 'POST'])
def login_hod():
    msg=""
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM fe_staff WHERE uname = %s AND pass = %s && stype='HOD'", (uname, pwd))
        account = cursor.fetchone()
        if account:
            #session['loggedin'] = True
            session['username'] = uname
            # Redirect to home page
            return redirect(url_for('hod_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('web/login_hod.html',msg=msg)


@app.route('/login_staff', methods=['GET', 'POST'])
def login_staff():
    msg=""
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM fe_staff WHERE uname = %s AND pass = %s && stype='Invigilator'", (uname, pwd))
        account = cursor.fetchone()
        if account:
            #session['loggedin'] = True
            session['username'] = uname
            # Redirect to home page
            return redirect(url_for('staff_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('web/login_staff.html',msg=msg)

@app.route('/admin',methods=['POST','GET'])
def admin():
    data=[]
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM fe_register")
    data = mycursor.fetchall()

    mycursor.execute("SELECT * FROM fe_department")
    value1 = mycursor.fetchall()

    mycursor.execute("SELECT distinct(year) FROM fe_register")
    value2 = mycursor.fetchall()

    if request.method=='POST':
        dept=request.form['dept']
        year=request.form['year']
        if dept!="" and year!="":
            mycursor.execute("SELECT * FROM fe_register where dept=%s && year=%s",(dept,year))
            data = mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM fe_register")
        data = mycursor.fetchall()

    ###
    if act=="del":
        did=request.args.get("did")

        mycursor.execute("delete from fe_register where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('admin')) 
    ###
        
    return render_template('admin.html',data=data,value1=value1,value2=value2)

@app.route('/admin2',methods=['POST','GET'])
def admin2():
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM train_data")
    value = mycursor.fetchall()

    ###
    if act=="del":
        did=request.args.get("did")

        mycursor.execute("SELECT count(*) FROM vt_face where vid=%s",(did,))
        cn = mycursor.fetchone()[0]
        if cn>0:
            mycursor.execute("SELECT * FROM vt_face where vid=%s",(did,))
            dd = mycursor.fetchall()
            for ds in dd:
                os.remove("static/frame/"+ds[2])
                os.remove("images_db/"+ds[2])

            mycursor.execute("delete from vt_face where vid=%s",(did,))
            mydb.commit()
                
        
        mycursor.execute("delete from train_data where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('admin')) 
    ###
        
    return render_template('admin2.html',value=value)


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')




@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    #import student
    msg=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM fe_department")
    value1 = mycursor.fetchall()
    
    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        aadhar=request.form['aadhar']
        regno=request.form['regno']
        dept=request.form['dept']
        year=request.form['year']
        

        mycursor.execute("SELECT count(*) FROM fe_register where regno=%s",(regno,))
        cnt = mycursor.fetchone()[0]

        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM fe_register")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

                
            sql = "INSERT INTO fe_register(id,name,mobile,email,address,aadhar,regno,dept,year,gender,dob) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s)"
            val = (maxid,name,mobile,email,address,aadhar,regno,dept,year,gender,dob)
            mycursor.execute(sql, val)
            mydb.commit()            
            return redirect(url_for('add_photo',vid=maxid)) 
        else:        
      
            msg='fail'

            
    return render_template('add_student.html',msg=msg,value1=value1)

@app.route('/add_staff',methods=['POST','GET'])
def add_staff():
    msg=""
    act=""
    mess=""
    email=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM fe_department")
    value1 = mycursor.fetchall()

    mycursor.execute("SELECT distinct(year) FROM fe_register")
    value2 = mycursor.fetchall()
    
    if request.method=='POST':
        
        uname=request.form['uname']
        name=request.form['name']       
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']        
        pass1=request.form['pass']
        stype=request.form['stype']
        dept=request.form['dept']
       
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM fe_staff where uname=%s",(uname, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM fe_staff")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO fe_staff(id, name, mobile, email, location,  uname, pass,stype,rdate,dept) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
            val = (maxid, name, mobile, email, location, uname, pass1,stype,rdate,dept)
            
            
            mycursor.execute(sql, val)
            mydb.commit()

            msg="success"
            mess="Dear "+name+", Staff ID: "+uname+" ("+stype+"), Password: "+pass1
            print(mycursor.rowcount, "record inserted.")
           
        else:
            msg="fail"
            
    return render_template('add_staff.html',msg=msg,act=act,value1=value1,value2=value2,mess=mess,email=email)


@app.route('/add_dept',methods=['POST','GET'])
def add_dept():
    msg=""
    act=request.args.get("act")
    mess=""
    email=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM fe_department")
    value1 = mycursor.fetchall()

    mycursor.execute("SELECT distinct(year) FROM fe_register")
    value2 = mycursor.fetchall()
    
    if request.method=='POST':
 
        dept=request.form['dept']
       


        mycursor.execute("SELECT count(*) FROM fe_department where department=%s",(dept, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM fe_department")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO fe_department(id,department) VALUES (%s, %s)"
            val = (maxid, dept)
            
            
            mycursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('add_dept')) 
           
        else:
            msg="fail"

    mycursor.execute("SELECT * FROM fe_department")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from fe_department where id=%s",(did,))
        mydb.commit()
        msg="ok"

        
    return render_template('add_dept.html',msg=msg,act=act,data=data)

@app.route('/add_hall',methods=['POST','GET'])
def add_hall():
    msg=""
    act=request.args.get("act")
    mess=""
    email=""
    mycursor = mydb.cursor()
    

    
    if request.method=='POST':
 
        hall=request.form['hall']
        seats=request.form['seats']


        mycursor.execute("SELECT max(id)+1 FROM fe_hall")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO fe_hall(id,hall,seats) VALUES (%s, %s, %s)"
        val = (maxid, hall, seats)
        
        
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('add_hall')) 
           
 
    mycursor.execute("SELECT * FROM fe_hall")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from fe_hall where id=%s",(did,))
        mydb.commit()
        msg="ok"

        
    return render_template('add_hall.html',msg=msg,act=act,data=data)

@app.route('/add_exam',methods=['POST','GET'])
def add_exam():
    msg=""
    act=request.args.get("act")
    mess=""
    email=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM fe_department")
    value1 = mycursor.fetchall()

    
    if request.method=='POST':
 
        dept=request.form['dept']
        exam=request.form['exam']


        mycursor.execute("SELECT max(id)+1 FROM fe_exam")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO fe_exam(id,dept,exam) VALUES (%s, %s, %s)"
        val = (maxid, dept, exam)
        
        
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('add_exam')) 
           
 
    mycursor.execute("SELECT * FROM fe_exam")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from fe_exam where id=%s",(did,))
        mydb.commit()
        msg="ok"

        
    return render_template('add_exam.html',msg=msg,act=act,data=data,value1=value1)

@app.route('/add_table', methods=['GET', 'POST'])
def add_table():
    act=request.args.get("act")
    msg=""
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM fe_staff where stype='Invigilator'")
    sdat = mycursor.fetchall()

    mycursor.execute("SELECT * FROM fe_department")
    mdat = mycursor.fetchall()

    mycursor.execute("SELECT * FROM fe_hall")
    hdat = mycursor.fetchall()

    exam=""
    mycursor.execute("SELECT * FROM fe_exam order by id desc")
    edat = mycursor.fetchall()
    for edat1 in edat:
        exam=edat1[2]
    
    if request.method=='POST':
        dept=request.form['dept']
        staff=request.form['staff']
        hall=request.form['hall']
        scode=request.form['scode']
        subject=request.form['subject']
        
        exam_time=request.form['exam_time']
        edate=request.form['edate']
        ed=edate.split("-")
        edate1=ed[2]+"-"+ed[1]+"-"+ed[0]
        
        mycursor.execute("SELECT max(id)+1 FROM fe_timetable")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO fe_timetable(id,dept,hall,staff,scode,subject,exam_time,edate,exam) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
        val = (maxid, dept, hall, staff, scode, subject, exam_time, edate1,exam)
        
        
        mycursor.execute(sql, val)
        mydb.commit()
        ####
        i=1
        mycursor.execute("SELECT * FROM fe_register where dept=%s",(dept,))
        fdat = mycursor.fetchall()
        for fdat1 in fdat:
            mycursor.execute("update fe_register set hall=%s,seat=%s where regno=%s",(hall,i,fdat1[13]))
            mydb.commit()
            i+=2
        
        msg="success"

    mycursor.execute("SELECT * FROM fe_timetable")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from fe_timetable where id=%s",(did,))
        mydb.commit()
        msg="ok"

            
    return render_template('add_table.html',msg=msg,act=act,sdat=sdat,mdat=mdat,hdat=hdat,data=data)




@app.route('/hod_home',methods=['POST','GET'])
def hod_home():
    data=[]
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM fe_register")
    data = mycursor.fetchall()

    mycursor.execute("SELECT * FROM fe_department")
    value1 = mycursor.fetchall()

    mycursor.execute("SELECT distinct(year) FROM fe_register")
    value2 = mycursor.fetchall()

    if request.method=='POST':
        dept=request.form['dept']
        year=request.form['year']
        if dept!="" and year!="":
            mycursor.execute("SELECT * FROM fe_register where dept=%s && year=%s",(dept,year))
            data = mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM fe_register")
        data = mycursor.fetchall()

   
        
    return render_template('hod_home.html',data=data,value1=value1,value2=value2)


@app.route('/staff_home',methods=['POST','GET'])
def staff_home():
    data=[]
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM fe_register")
    data = mycursor.fetchall()

    mycursor.execute("SELECT * FROM fe_department")
    value1 = mycursor.fetchall()

    mycursor.execute("SELECT distinct(year) FROM fe_register")
    value2 = mycursor.fetchall()

    ############
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor.execute('SELECT count(*) FROM fe_attendance where rdate=%s',(rdate,))
    cnt = mycursor.fetchone()[0]

    if cnt==0:
        
        mycursor.execute('SELECT * FROM fe_register')
        drow = mycursor.fetchall()

        for rw in drow:
            regno=rw[13]
            mycursor.execute("SELECT max(id)+1 FROM fe_attendance")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            sql = "INSERT INTO fe_attendance(id, regno, rdate, attendance, mask_st) VALUES (%s, %s, %s, %s, %s)"
            val = (maxid, regno, rdate, 'Absent', '-')
            print(sql)
            mycursor.execute(sql, val)
            mydb.commit()
    ############

    if request.method=='POST':
        dept=request.form['dept']
        year=request.form['year']
        if dept!="" and year!="":
            mycursor.execute("SELECT * FROM fe_register where dept=%s && year=%s",(dept,year))
            data = mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM fe_register")
        data = mycursor.fetchall()

   
        
    return render_template('staff_home.html',data=data,value1=value1,value2=value2)


@app.route('/staff_verify',methods=['POST','GET'])
def staff_verify():
    data=[]
    data2=[]
    s1=""
    regno=""
    vid=""
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM fe_register")
    data = mycursor.fetchall()


    ############
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    ff=open("static/sms.txt","w")
    ff.write("1")
    ff.close()
    ############

    if request.method=='POST':
        regno=request.form['regno']
        
        mycursor.execute("SELECT count(*) FROM fe_register where regno=%s",(regno,))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            s1="1"
            mycursor.execute("SELECT * FROM fe_register where regno=%s",(regno,))
            data = mycursor.fetchone()
            dept=data[6]
            vid=str(data[0])

            mycursor.execute("SELECT count(*) FROM fe_timetable where dept=%s && edate=%s",(dept,rdate))
            dd = mycursor.fetchone()[0]

            if dd>0:
                mycursor.execute("SELECT * FROM fe_timetable where dept=%s && edate=%s limit 0,1",(dept,rdate))
                data2 = mycursor.fetchall()
            else:

                s1="3"
            
        
        else:
            s1="2"

   
        
    return render_template('staff_verify.html',s1=s1,regno=regno,data=data,data2=data2,vid=vid)


@app.route('/view_att',methods=['POST','GET'])
def view_att():
    msg=""
    uname=""
    st=""
    act=request.args.get("act")
    data=[]

    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM fe_staff where uname=%s",(uname,))
    data1 = cursor.fetchone()
    email=data1[3]
    
    if request.method=='POST':
        
        rd=request.form['rdate']
        rdd=rd.split('-')
        rdate=rdd[2]+"-"+rdd[1]+"-"+rdd[0]
        cursor.execute('SELECT count(*) FROM fe_attendance where rdate=%s',(rdate,))
        cnt = cursor.fetchone()[0]

        if cnt>0:
            act="1"
            cursor.execute('SELECT * FROM fe_attendance a,fe_register r where a.rdate=%s && a.regno=r.regno',(rdate,))
            data = cursor.fetchall()

   
    return render_template('view_att.html',msg=msg,act=act,data=data,st=st)

@app.route('/view_report',methods=['POST','GET'])
def view_report():
    msg=""
    uname=""
    act=request.args.get("act")
    data=[]

    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM fe_staff where uname=%s",(uname,))
    data1 = mycursor.fetchone()
    dept=data1[9]

    mycursor.execute("SELECT * FROM fe_detect where dept=%s order by id desc",(dept,))
    data = mycursor.fetchall()



        
    return render_template('view_report.html',data=data)


@app.route('/view_staff', methods=['GET', 'POST'])
def view_staff():
    #import student
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM fe_staff")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from fe_staff where id=%s",(did,))
        mydb.commit()
        msg="ok"

    return render_template('view_staff.html',msg=msg,act=act,data=data)


@app.route('/view_table', methods=['GET', 'POST'])
def view_table():
    #import student
    msg=""
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM fe_timetable")
    data = mycursor.fetchall()

    return render_template('view_table.html',msg=msg,data=data)


def getImagesAndLabels(path):

    
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids


@app.route('/add_photo',methods=['POST','GET'])
def add_photo():
    vid = request.args.get('vid')
    ff1=open("photo.txt","w")
    ff1.write("2")
    ff1.close()

    #ff2=open("mask.txt","w")
    #ff2.write("face")
    #ff2.close()
    act = request.args.get('act')

    cursor = mydb.cursor()
    
    cursor.execute("SELECT * FROM fe_register where id=%s",(vid,))
    value = cursor.fetchone()
    name=value[1]
    
    ff=open("user.txt","w")
    ff.write(name)
    ff.close()

    ff=open("user1.txt","w")
    ff.write(vid)
    ff.close()
    

    
    
    if request.method=='POST':
        vid=request.form['vid']
        fimg="v"+vid+".jpg"
        

        cursor.execute('delete from fe_face WHERE vid = %s', (vid, ))
        mydb.commit()

        

        ff=open("det.txt","r")
        v=ff.read()
        ff.close()
        vv=int(v)
        v1=vv-1
        vface1="User."+vid+"."+str(v1)+".jpg"
        i=2
        while i<vv:
            
            cursor.execute("SELECT max(id)+1 FROM fe_face")
            maxid = cursor.fetchone()[0]
            if maxid is None:
                maxid=1
            vface="User."+vid+"."+str(i)+".jpg"
            sql = "INSERT INTO fe_face(id, vid, vface) VALUES (%s, %s, %s)"
            val = (maxid, vid, vface)
            print(val)
            cursor.execute(sql,val)
            mydb.commit()
            i+=1

        
            
        cursor.execute('update fe_register set fimg=%s WHERE id = %s', (vface1, vid))
        mydb.commit()
        shutil.copy('static/faces/f1.jpg', 'static/photo/'+vface1)

        
        ##########
        
        ##Training face
        # Path for face image database
        path = 'dataset'

        recognizer = cv2.face.LBPHFaceRecognizer_create()

        # function to get the images and label data
        

        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))






        #################################################
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM fe_face where vid=%s",(vid, ))
        dt = cursor.fetchall()
        for rs in dt:
            ##Preprocess
            path="static/frame/"+rs[2]
            path2="static/process1/"+rs[2]
            mm2 = PIL.Image.open(path).convert('L')
            rz = mm2.resize((200,200), PIL.Image.ANTIALIAS)
            rz.save(path2)
            
            '''img = cv2.imread(path2) 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            path3="static/process2/"+rs[2]
            cv2.imwrite(path3, dst)'''
            #noice
            img = cv2.imread('static/process1/'+rs[2]) 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            fname2='ns_'+rs[2]
            cv2.imwrite("static/process1/"+fname2, dst)
            ######
            ##bin
            image = cv2.imread('static/process1/'+rs[2])
            original = image.copy()
            kmeans = kmeans_color_quantization(image, clusters=4)

            # Convert to grayscale, Gaussian blur, adaptive threshold
            gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3,3), 0)
            thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)
            
            # Draw largest enclosing circle onto a mask
            mask = np.zeros(original.shape[:2], dtype=np.uint8)
            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
            for c in cnts:
                ((x, y), r) = cv2.minEnclosingCircle(c)
                cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
                cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
                break
            
            # Bitwise-and for result
            result = cv2.bitwise_and(original, original, mask=mask)
            result[mask==0] = (0,0,0)

            
            ###cv2.imshow('thresh', thresh)
            ###cv2.imshow('result', result)
            ###cv2.imshow('mask', mask)
            ###cv2.imshow('kmeans', kmeans)
            ###cv2.imshow('image', image)
            ###cv2.waitKey()

            cv2.imwrite("static/process1/bin_"+rs[2], thresh)
            

            ###RPN - Segment
            img = cv2.imread('static/process1/'+rs[2])
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/fg_"+rs[2]
            segment.save(path3)
            ####
            img = cv2.imread('static/process2/fg_'+rs[2])
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/fg_"+rs[2]
            segment.save(path3)
            '''
            img = cv2.imread(path2)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # noise removal
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/"+rs[2]
            segment.save(path3)
            '''
            #####
            image = cv2.imread(path2)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            image = Image.fromarray(image)
            edged = Image.fromarray(edged)
            path4="static/process3/"+rs[2]
            edged.save(path4)
            ##
        ###
        cursor.execute("SELECT count(*) FROM fe_face where vid=%s",(vid, ))
        cnt = cursor.fetchone()[0]
        
        return redirect(url_for('view_photo',vid=vid,act='success'))
        
    
    cursor.execute("SELECT * FROM fe_register")
    data = cursor.fetchall()
    return render_template('add_photo.html',data=data, vid=vid)

def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

@app.route('/view_photo',methods=['POST','GET'])
def view_photo():
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM fe_face where vid=%s",(vid, ))
        value = mycursor.fetchall()

    if request.method=='POST':
        print("Training")
        vid=request.form['vid']
        
        #shutil.copy('static/img/11.png', 'static/process4/'+rs[2])
       
        #return redirect(url_for('view_photo1',vid=vid))
        
    return render_template('view_photo.html', result=value,vid=vid)



@app.route('/pro1',methods=['POST','GET'])
def pro1():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM fe_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM fe_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('pro1.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro2',methods=['POST','GET'])
def pro2():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM fe_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None or act=='0':
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM fe_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('pro2.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro3',methods=['POST','GET'])
def pro3():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM fe_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM fe_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('pro3.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro4',methods=['POST','GET'])
def pro4():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM fe_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM fe_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('pro4.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro5',methods=['POST','GET'])
def pro5():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM fe_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM fe_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('pro5.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro6',methods=['POST','GET'])
def pro6():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM fe_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM fe_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('pro6.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro7',methods=['POST','GET'])
def pro7():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM fe_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM fe_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('pro7.html', value=value,vid=vid, act=act3,s1=s1)

def CNN():
    #Lets start by loading the Cifar10 data
    (X, y), (X_test, y_test) = cifar10.load_data()

    #Keep in mind the images are in RGB
    #So we can normalise the data by diving by 255
    #The data is in integers therefore we need to convert them to float first
    X, X_test = X.astype('float32')/255.0, X_test.astype('float32')/255.0

    #Then we convert the y values into one-hot vectors
    #The cifar10 has only 10 classes, thats is why we specify a one-hot
    #vector of width/class 10
    y, y_test = u.to_categorical(y, 10), u.to_categorical(y_test, 10)

    #Now we can go ahead and create our Convolution model
    model = Sequential()
    #We want to output 32 features maps. The kernel size is going to be
    #3x3 and we specify our input shape to be 32x32 with 3 channels
    #Padding=same means we want the same dimensional output as input
    #activation specifies the activation function
    model.add(Conv2D(32, (3, 3), input_shape=(32, 32, 3), padding='same',
                     activation='relu'))
    #20% of the nodes are set to 0
    model.add(Dropout(0.2))
    #now we add another convolution layer, again with a 3x3 kernel
    #This time our padding=valid this means that the output dimension can
    #take any form
    model.add(Conv2D(32, (3, 3), activation='relu', padding='valid'))
    #maxpool with a kernet of 2x2
    model.add(MaxPooling2D(pool_size=(2, 2)))
    #In a convolution NN, we neet to flatten our data before we can
    #input it into the ouput/dense layer
    model.add(Flatten())
    #Dense layer with 512 hidden units
    model.add(Dense(512, activation='relu'))
    #this time we set 30% of the nodes to 0 to minimize overfitting
    model.add(Dropout(0.3))
    #Finally the output dense layer with 10 hidden units corresponding to
    #our 10 classe
    model.add(Dense(10, activation='softmax'))
    #Few simple configurations
    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(momentum=0.5, decay=0.0004), metrics=['accuracy'])
    #Run the algorithm!
    model.fit(X, y, validation_data=(X_test, y_test), epochs=25,
              batch_size=512)
    #Save the weights to use for later
    model.save_weights("cifar10.hdf5")
    #Finally print the accuracy of our model!
    print("Accuracy: &2.f%%" %(model.evaluate(X_test, y_test)[1]*100))



##FR-CNN
def FRCNN(): 
    C.use_horizontal_flips = bool(options.horizontal_flips)
    C.use_vertical_flips = bool(options.vertical_flips)
    C.rot_90 = bool(options.rot_90)

    C.model_path = options.output_weight_path
    model_path_regex = re.match("^(.+)(\.hdf5)$", C.model_path)
    if model_path_regex.group(2) != '.hdf5':
        print('Output weights must have .hdf5 filetype')
        exit(1)
    C.num_rois = int(options.num_rois)

    if options.network == 'vgg':
        C.network = 'vgg'
        from keras_frcnn import vgg as nn
    elif options.network == 'resnet50':
        from keras_frcnn import resnet as nn
        C.network = 'resnet50'
    else:
        print('Not a valid model')
        raise ValueError


    # check if weight path was passed via command line
    if options.input_weight_path:
        C.base_net_weights = options.input_weight_path
    else:
        # set the path to weights based on backend and model
        C.base_net_weights = nn.get_weight_path()

    train_imgs, classes_count, class_mapping = get_data(options.train_path)
    val_imgs, _, _ = get_data(options.train_path)

    if 'bg' not in classes_count:
        classes_count['bg'] = 0
        class_mapping['bg'] = len(class_mapping)

    C.class_mapping = class_mapping

    inv_map = {v: k for k, v in class_mapping.items()}

    print('Training images per class:')
    pprint.pprint(classes_count)
    print(f'Num classes (including bg) = {len(classes_count)}')

    config_output_filename = options.config_filename

    with open(config_output_filename, 'wb') as config_f:
        pickle.dump(C,config_f)
        print(f'Config has been written to {config_output_filename}, and can be loaded when testing to ensure correct results')

    random.shuffle(train_imgs)

    num_imgs = len(train_imgs)

    #train_imgs = [s for s in all_imgs if s['imageset'] == 'trainval']
    #val_imgs = [s for s in all_imgs if s['imageset'] == 'test']

    print(f'Num train samples {len(train_imgs)}')
    print(f'Num val samples {len(val_imgs)}')


    data_gen_train = data_generators.get_anchor_gt(train_imgs, classes_count, C, nn.get_img_output_length, K.common.image_dim_ordering(), mode='train')
    data_gen_val = data_generators.get_anchor_gt(val_imgs, classes_count, C, nn.get_img_output_length,K.common.image_dim_ordering(), mode='val')

    if K.common.image_dim_ordering() == 'th':
        input_shape_img = (3, None, None)
    else:
        input_shape_img = (None, None, 3)

    img_input = Input(shape=input_shape_img)
    roi_input = Input(shape=(None, 4))

    # define the base network (resnet here, can be VGG, Inception, etc)
    shared_layers = nn.nn_base(img_input, trainable=True)

    # define the RPN, built on the base layers
    num_anchors = len(C.anchor_box_scales) * len(C.anchor_box_ratios)
    rpn = nn.rpn(shared_layers, num_anchors)

    classifier = nn.classifier(shared_layers, roi_input, C.num_rois, nb_classes=len(classes_count), trainable=True)

    model_rpn = Model(img_input, rpn[:2])
    model_classifier = Model([img_input, roi_input], classifier)

    # this is a model that holds both the RPN and the classifier, used to load/save weights for the models
    model_all = Model([img_input, roi_input], rpn[:2] + classifier)

    try:
        print('loading weights from {C.base_net_weights}')
        model_rpn.load_weights(C.base_net_weights, by_name=True)
        model_classifier.load_weights(C.base_net_weights, by_name=True)
    except:
        print('Could not load pretrained model weights. Weights can be found in the keras application folder ')

    optimizer = Adam(lr=1e-5)
    optimizer_classifier = Adam(lr=1e-5)
    model_rpn.compile(optimizer=optimizer, loss=[losses.rpn_loss_cls(num_anchors), losses.rpn_loss_regr(num_anchors)])
    model_classifier.compile(optimizer=optimizer_classifier, loss=[losses.class_loss_cls, losses.class_loss_regr(len(classes_count)-1)], metrics={f'dense_class_{len(classes_count)}': 'accuracy'})
    model_all.compile(optimizer='sgd', loss='mae')

    epoch_length = num_imgs
    num_epochs = int(options.num_epochs)
    iter_num = 0

    losses = np.zeros((epoch_length, 5))
    rpn_accuracy_rpn_monitor = []
    rpn_accuracy_for_epoch = []
    start_time = time.time()

    best_loss = np.Inf

    class_mapping_inv = {v: k for k, v in class_mapping.items()}
    print('Starting training')

    vis = True

    for epoch_num in range(num_epochs):

        progbar = generic_utils.Progbar(epoch_length)
        print(f'Epoch {epoch_num + 1}/{num_epochs}')

        while True:
            try:

                if len(rpn_accuracy_rpn_monitor) == epoch_length and C.verbose:
                    mean_overlapping_bboxes = float(sum(rpn_accuracy_rpn_monitor))/len(rpn_accuracy_rpn_monitor)
                    rpn_accuracy_rpn_monitor = []
                    print(f'Average number of overlapping bounding boxes from RPN = {mean_overlapping_bboxes} for {epoch_length} previous iterations')
                    if mean_overlapping_bboxes == 0:
                        print('RPN is not producing bounding boxes that overlap the ground truth boxes. Check RPN settings or keep training.')

                X, Y, img_data = next(data_gen_train)

                loss_rpn = model_rpn.train_on_batch(X, Y)

                P_rpn = model_rpn.predict_on_batch(X)

                R = roi_helpers.rpn_to_roi(P_rpn[0], P_rpn[1], C, K.common.image_dim_ordering(), use_regr=True, overlap_thresh=0.7, max_boxes=300)
                # note: calc_iou converts from (x1,y1,x2,y2) to (x,y,w,h) format
                X2, Y1, Y2, IouS = roi_helpers.calc_iou(R, img_data, C, class_mapping)

                if X2 is None:
                    rpn_accuracy_rpn_monitor.append(0)
                    rpn_accuracy_for_epoch.append(0)
                    continue

                neg_samples = np.where(Y1[0, :, -1] == 1)
                pos_samples = np.where(Y1[0, :, -1] == 0)

                if len(neg_samples) > 0:
                    neg_samples = neg_samples[0]
                else:
                    neg_samples = []

                if len(pos_samples) > 0:
                    pos_samples = pos_samples[0]
                else:
                    pos_samples = []

                rpn_accuracy_rpn_monitor.append(len(pos_samples))
                rpn_accuracy_for_epoch.append((len(pos_samples)))

                if C.num_rois > 1:
                    if len(pos_samples) < C.num_rois//2:
                        selected_pos_samples = pos_samples.tolist()
                    else:
                        selected_pos_samples = np.random.choice(pos_samples, C.num_rois//2, replace=False).tolist()
                    try:
                        selected_neg_samples = np.random.choice(neg_samples, C.num_rois - len(selected_pos_samples), replace=False).tolist()
                    except:
                        selected_neg_samples = np.random.choice(neg_samples, C.num_rois - len(selected_pos_samples), replace=True).tolist()

                    sel_samples = selected_pos_samples + selected_neg_samples
                else:
                    # in the extreme case where num_rois = 1, we pick a random pos or neg sample
                    selected_pos_samples = pos_samples.tolist()
                    selected_neg_samples = neg_samples.tolist()
                    if np.random.randint(0, 2):
                        sel_samples = random.choice(neg_samples)
                    else:
                        sel_samples = random.choice(pos_samples)

                loss_class = model_classifier.train_on_batch([X, X2[:, sel_samples, :]], [Y1[:, sel_samples, :], Y2[:, sel_samples, :]])

                losses[iter_num, 0] = loss_rpn[1]
                losses[iter_num, 1] = loss_rpn[2]

                losses[iter_num, 2] = loss_class[1]
                losses[iter_num, 3] = loss_class[2]
                losses[iter_num, 4] = loss_class[3]

                progbar.update(iter_num+1, [('rpn_cls', losses[iter_num, 0]), ('rpn_regr', losses[iter_num, 1]),
                                          ('detector_cls', losses[iter_num, 2]), ('detector_regr', losses[iter_num, 3])])

                iter_num += 1
                
                if iter_num == epoch_length:
                    loss_rpn_cls = np.mean(losses[:, 0])
                    loss_rpn_regr = np.mean(losses[:, 1])
                    loss_class_cls = np.mean(losses[:, 2])
                    loss_class_regr = np.mean(losses[:, 3])
                    class_acc = np.mean(losses[:, 4])

                    mean_overlapping_bboxes = float(sum(rpn_accuracy_for_epoch)) / len(rpn_accuracy_for_epoch)
                    rpn_accuracy_for_epoch = []

                    if C.verbose:
                        print(f'Mean number of bounding boxes from RPN overlapping ground truth boxes: {mean_overlapping_bboxes}')
                        print(f'Classifier accuracy for bounding boxes from RPN: {class_acc}')
                        print(f'Loss RPN classifier: {loss_rpn_cls}')
                        print(f'Loss RPN regression: {loss_rpn_regr}')
                        print(f'Loss Detector classifier: {loss_class_cls}')
                        print(f'Loss Detector regression: {loss_class_regr}')
                        print(f'Elapsed time: {time.time() - start_time}')

                    curr_loss = loss_rpn_cls + loss_rpn_regr + loss_class_cls + loss_class_regr
                    iter_num = 0
                    start_time = time.time()

                    if curr_loss < best_loss:
                        if C.verbose:
                            print(f'Total loss decreased from {best_loss} to {curr_loss}, saving weights')
                        best_loss = curr_loss
                    model_all.save_weights(model_path_regex.group(1) + "_" + '{:04d}'.format(epoch_num) + model_path_regex.group(2))

                    break

            except Exception as e:
                print(f'Exception: {e}')
                continue

def get_real_coordinates():
    img_input = Input(shape=input_shape_img)
    roi_input = Input(shape=(C.num_rois, 4))
    feature_map_input = Input(shape=input_shape_features)

    # define the base network (resnet here, can be VGG, Inception, etc)
    shared_layers = nn.nn_base(img_input, trainable=True)

    # define the RPN, built on the base layers
    num_anchors = len(C.anchor_box_scales) * len(C.anchor_box_ratios)
    rpn_layers = nn.rpn(shared_layers, num_anchors)

    classifier = nn.classifier(feature_map_input, roi_input, C.num_rois, nb_classes=len(class_mapping), trainable=True)

    model_rpn = Model(img_input, rpn_layers)
    model_classifier_only = Model([feature_map_input, roi_input], classifier)

    model_classifier = Model([feature_map_input, roi_input], classifier)

    print(f'Loading weights from {C.model_path}')
    model_rpn.load_weights(C.model_path, by_name=True)
    model_classifier.load_weights(C.model_path, by_name=True)

    model_rpn.compile(optimizer='sgd', loss='mse')
    model_classifier.compile(optimizer='sgd', loss='mse')

    all_imgs = []

    classes = {}

    bbox_threshold = 0.8

    visualise = True

    for idx, img_name in enumerate(sorted(os.listdir(img_path))):

            file_count0+=1
            if int(os.path.splitext(img_name)[0]) < avg_delta_calculation_boundary1: #2xxx
                    file_count1+=1
            elif int(os.path.splitext(img_name)[0]) < avg_delta_calculation_boundary2: #5xxx
                    file_count2+=1
            elif int(os.path.splitext(img_name)[0]) < avg_delta_calculation_boundary3: #6xxx
                    file_count3+=1
            else: #7xxx
                    file_count4+=1
            if file_count0 != file_count1+file_count2+file_count3+file_count4:
                    print('\nfile number error\n')
                    break

            if not img_name.lower().endswith(('.bmp', '.jpeg', '.jpg', '.png', '.tif', '.tiff')):
                    continue
            print(img_name)
            st = time.time()
            filepath = os.path.join(img_path,img_name)

            img = cv2.imread(filepath)

            X, ratio = format_img(img, C)

            if K.common.image_dim_ordering() == 'tf':
                    X = np.transpose(X, (0, 2, 3, 1))

            # get the feature maps and output from the RPN
            [Y1, Y2, F] = model_rpn.predict(X)
            

            R = roi_helpers.rpn_to_roi(Y1, Y2, C, K.common.image_dim_ordering(), overlap_thresh=0.7)

            # convert from (x1,y1,x2,y2) to (x,y,w,h)
            R[:, 2] -= R[:, 0]
            R[:, 3] -= R[:, 1]

            # apply the spatial pyramid pooling to the proposed regions
            bboxes = {}
            probs = {}

            for jk in range(R.shape[0] // C.num_rois + 1):

                    ROIs = np.expand_dims(R[C.num_rois * jk:C.num_rois * (jk + 1), :], axis=0)
                    if ROIs.shape[1] == 0:
                            break

                    if jk == R.shape[0] // C.num_rois:
                            #pad R
                            curr_shape = ROIs.shape
                            target_shape = (curr_shape[0],C.num_rois,curr_shape[2])
                            ROIs_padded = np.zeros(target_shape).astype(ROIs.dtype)
                            ROIs_padded[:, :curr_shape[1], :] = ROIs
                            ROIs_padded[0, curr_shape[1]:, :] = ROIs[0, 0, :]
                            ROIs = ROIs_padded

                    [P_cls, P_regr] = model_classifier_only.predict([F, ROIs])

                    for ii in range(P_cls.shape[1]):

                            if np.max(P_cls[0, ii, :]) < bbox_threshold or np.argmax(P_cls[0, ii, :]) == (P_cls.shape[2] - 1):
                                    continue

                            cls_name = class_mapping[np.argmax(P_cls[0, ii, :])]

                            if cls_name not in bboxes:
                                    bboxes[cls_name] = []
                                    probs[cls_name] = []

                            (x, y, w, h) = ROIs[0, ii, :]

                            cls_num = np.argmax(P_cls[0, ii, :])
                            try:
                                    (tx, ty, tw, th) = P_regr[0, ii, 4 * cls_num:4 * (cls_num + 1)]
                                    tx /= C.classifier_regr_std[0]
                                    ty /= C.classifier_regr_std[1]
                                    tw /= C.classifier_regr_std[2]
                                    th /= C.classifier_regr_std[3]
                                    x, y, w, h = roi_helpers.apply_regr(x, y, w, h, tx, ty, tw, th)
                            except:
                                    pass
                            bboxes[cls_name].append([C.rpn_stride * x, C.rpn_stride * y, C.rpn_stride * (x + w), C.rpn_stride * (y + h)])
                            probs[cls_name].append(np.max(P_cls[0, ii, :]))

            all_dets = []

            for key in bboxes:
                    bbox = np.array(bboxes[key])

                    new_boxes, new_probs = roi_helpers.non_max_suppression_fast(bbox, np.array(probs[key]), overlap_thresh=0.5)
                    for jk in range(new_boxes.shape[0]):
                            (x1, y1, x2, y2) = new_boxes[jk,:]

                            (real_x1, real_y1, real_x2, real_y2) = get_real_coordinates(ratio, x1, y1, x2, y2)

                            cv2.rectangle(img,(real_x1, real_y1), (real_x2, real_y2), (int(class_to_color[key][0]), int(class_to_color[key][1]), int(class_to_color[key][2])),2)

                            textLabel = f'{key}: {int(100*new_probs[jk])}'
                            all_dets.append((key,100 * new_probs[jk]))

                            #export x1, y1, x2, y2 coordinate data
                            coordinate_count0+=1
                            if int(os.path.splitext(img_name)[0]) < avg_delta_calculation_boundary1: #2xxx
                                    coordinate_count1 = coordinate_count0
                                    object_identified_flag1 = True
                                    train_avg_delta_x1 = (train_avg_delta_x1 + (real_x2 - real_x1)) / 2
                                    train_avg_delta_y1 = (train_avg_delta_y1 + (real_y2 - real_y1)) / 2
                                    rows.append([img_name,
                                                             textLabel,
                                                             digit_format.format(real_x1),
                                                         digit_format.format(real_y1),
                                                         digit_format.format(real_x2),
                                                         digit_format.format(real_y2),
                                                         digit_format.format((real_x1 + real_x2) / 2),
                                                     digit_format.format((real_y1 + real_y2) / 2),
                                                     digit_format.format(real_x2 - real_x1),
                                                     digit_format.format(real_y2 - real_y1),
                                                     digit_format.format(real_x2 - real_x1 - train_avg_delta_x1),
                                                 digit_format.format(real_y2 - real_y1 - train_avg_delta_y1)])
				
##

@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
    
    cam1=request.args.get("cam1")
    cam2=request.args.get("cam2")
    cam3=request.args.get("cam3")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM admin")
    value = mycursor.fetchone()

    ff=open("static/sms.txt","w")
    ff.write("1")
    ff.close()

    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    mycursor.execute('SELECT count(*) FROM fe_attendance where rdate=%s',(rdate,))
    cnt = mycursor.fetchone()[0]

    if cnt==0:
        
        mycursor.execute('SELECT * FROM register')
        drow = mycursor.fetchall()

        for rw in drow:
            regno=rw[13]
            mycursor.execute("SELECT max(id)+1 FROM fe_attendance")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            sql = "INSERT INTO fe_attendance(id, regno, rdate, attendance, mask_st) VALUES (%s, %s, %s, %s, %s)"
            val = (maxid, regno, rdate, 'Absent', '-')
            print(sql)
            mycursor.execute(sql, val)
            mydb.commit()
            

    return render_template('monitor.html',cam1=cam1,cam2=cam2,cam3=cam3,value=value)

@app.route('/staff_verify2',methods=['POST','GET'])
def staff_verify2():
    data=[]
    data2=[]
    s1=""
    regno=request.args.get("regno")
    vid=request.args.get("vid")
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM fe_register")
    data = mycursor.fetchall()


    ############
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
   
    ############

  
   
        
    return render_template('staff_verify2.html',s1=s1,regno=regno,vid=vid)

@app.route('/process1', methods=['GET', 'POST'])
def process1():
    s1=""
    regno=request.args.get("regno")
    vid=request.args.get("vid")

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
   

    return render_template('process1.html',regno=regno,vid=vid)

@app.route('/process11', methods=['GET', 'POST'])
def process11():
    st=""
    sms=""
    data=[]
    data2=[]
    mess=""
    mobile=""
    regno=request.args.get("regno")
    vid=request.args.get("vid")

    mycursor = mydb.cursor()

    ff=open("static/sms.txt","r")
    ss=ff.read()
    ff.close()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    ff=open("static/cam1.txt","r")
    uid=ff.read()
    ff.close()

    mycursor.execute("SELECT * FROM fe_register where id=%s",(vid,))
    data = mycursor.fetchone()
    name=data[1]
    dept=data[6]

    mycursor.execute("SELECT * FROM fe_staff where dept=%s && stype='HOD'",(dept,))
    data4 = mycursor.fetchone()
    mobile=data4[2]

    

    if vid==uid:
        st="1"

        

        mycursor.execute("SELECT * FROM fe_timetable where dept=%s && edate=%s",(dept,rdate))
        data2 = mycursor.fetchall()

        mycursor.execute("update fe_attendance set attendance='Present' where regno=%s && rdate=%s",(regno,rdate))
        mydb.commit()
    else:
        st="2"
        
        ss1=int(ss)+1
        if ss1<=3:
            sms="1"
            ff=open("static/sms.txt","w")
            ff.write(str(ss1))
            ff.close()
        mycursor.execute("SELECT max(id)+1 FROM fe_detect")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        fn="d"+str(maxid)+".jpg"
        shutil.copy("static/faces/f1.jpg","static/detect/"+fn)

        mess="RegNo.:"+regno+", Impersonation Student"
        
        sql = "INSERT INTO fe_detect(id, regno,name, face_img, dept) VALUES (%s, %s, %s, %s, %s)"
        val = (maxid,regno,name,fn,dept)
        
        mycursor.execute(sql, val)
        mydb.commit()
    
    
    return render_template('process11.html',regno=regno,vid=vid,st=st,data=data,data2=data2,sms=sms,mobile=mobile,mess=mess)

@app.route('/verify_cam', methods=['GET', 'POST'])
def verify_cam():
    s1=""
    

    return render_template('verify_cam.html')

@app.route('/process2', methods=['GET', 'POST'])
def process2():
    s1=""
    
    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
   

    return render_template('process2.html')

@app.route('/process22', methods=['GET', 'POST'])
def process22():
    st=""
    data=[]
    data2=[]
    

    mycursor = mydb.cursor()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    ff=open("static/cam1.txt","r")
    uid=ff.read()
    ff.close()

    

    if uid=="":
        st="2"
    else:
        st="1"
        mycursor.execute("SELECT * FROM fe_register where id=%s",(uid,))
        data = mycursor.fetchone()
        name=data[1]
        dept=data[6]

        mycursor.execute("SELECT * FROM fe_timetable where dept=%s && edate=%s",(dept,rdate))
        data2 = mycursor.fetchall()

   
    
    return render_template('process22.html',st=st,data=data,data2=data2)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))



#######
def gen2(camera):
    while True:
        frame = camera.get_frame()
    

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/video_feed2')
def video_feed2():

    return Response(gen2(VideoCamera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
##########
def gen(camera):

    while True:
        frame = camera.get_frame()
    

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    
@app.route('/video_feed')
def video_feed():
    
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#########
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
