from flask import Flask, render_template, request
import pymysql

RDS_ENDPOINT = 'testdb.cnr20hoyd3cu.ap-northeast-2.rds.amazonaws.com'
RDS_PORT = 3306
RDS_USER = 'root'
RDS_PASSWORD = 'password'
RDS_DATABASE = 'humandb'
RDS_TABLE = 'applicant'

# ---------RDS Connect--------------
conn = pymysql.connect(
    host=RDS_ENDPOINT,
    port=RDS_PORT,
    user=RDS_USER,
    password=RDS_PASSWORD,
    db=RDS_DATABASE
)


# --------Table Creation----------
def createTable():
    cursor = conn.cursor()
    create_table = f"create table {RDS_TABLE} (number int auto_increment primary key, name char(10) not null ,contact text not null ,resume text, blog text, result BOOLEAN)"
    try:
        cursor.execute(create_table)
    except:
        print('Table Already Exist')


# ------------INSERT QUERY----------
def insertHuman(name, contact, resume, blog):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {RDS_TABLE} (name,contact,resume,blog) VALUES (%s,%s,%s,%s)",
                (name, contact, resume, blog))
    conn.commit()


# -----------RDS INSERT FUNCTION---------
def insertData(name, email, comment, gender):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {RDS_TABLE} (name,contact,resume,blog) VALUES (%s,%s,%s,%s)",
                (name, email, comment, gender))
    conn.commit()


createTable()
server = Flask(__name__)


@server.route('/')
def submit():
    return render_template("submit.html")


@server.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        resume = request.form['resume']
        blog = request.form['blog']
        insertData(name, contact, resume, blog)
        return render_template('submit.html')


def echo_test():
    return 'success'
