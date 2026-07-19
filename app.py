from flask import Flask,render_template ,request,redirect,url_for
import pymysql
import os
import uuid
app = Flask(__name__)



UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def connect_db ():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        db="flask_template_2_5"
    )

    if not connection :
        print(" can not connect to database 🥲!")
    else:
        print(" coonnect to database success ! 🥳")    

    return connection



@app.route('/')
def index():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products ")
    user = cursor.fetchall() 

    return render_template("index.html",myuser = user)


@app.route('/insert',methods=['POST'])
def insert():
    connection = connect_db()
    cursor = connection.cursor()

    name = request.form['name']
    price = request.form['price']
    qty = request.form['qty']
    desctiption = request.form['description']
    image = request.files['image']

    new_name = ""

    if not image :
        print("image not found !")


    if image :
        split_image = os.path.split(image.filename)[1]
        new_name = str(uuid.uuid4()) + split_image
        image.save(os.path.join(app.config['UPLOAD_FOLDER'],new_name))



    sql = "INSERT INTO products (name,price,qty,description,image) VALUES (%s,%s,%s,%s,%s) "
    cursor.execute(sql,(name,price,qty,desctiption,new_name))

    connection.commit()

    return redirect(url_for("index"))


@app.route('/update',methods=['POST'])
def update():
    connection = connect_db()
    cursor = connection.cursor()
    id = request.form['update_id']
    name = request.form['update_name']
    age = request.form['update_age']
    gender = request.form['update_gender']
    grade = request.form['update_grade']


    sql = " UPDATE users SET NAME= %s  , AGE = %s , GENDER = %s , GRADE = %s WHERE ID = %s"
    cursor.execute(sql,(name,age,gender,grade,id))

    connection.commit()

    return redirect (url_for('index'))



@app.route('/delete',methods=["POST"])
def delete ():
    conection = connect_db()
    cursor = conection.cursor()
    id = request.form['delete_id']

    sql = "DELETE FROM users WHERE ID = %s"
    cursor.execute(sql,(id))
    conection.commit()


    return redirect(url_for('index'))



@app.route('/userpage')
def userpage ():
    myconnection = connect_db()
    cursor = myconnection.cursor()


    cursor.execute (" SELECT * FROM products")
    data = cursor.fetchall()

    return render_template ('userpage.html',data = data)

if __name__ == "__main__":
    app.run(debug=True)


