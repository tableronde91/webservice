from collections import defaultdict
from flask import Flask,render_template, request,jsonify
from flask_mysqldb import MySQL

with open("codehypersecret.fuck") as file:
    mdp = file.read()
iiens = True

app = Flask(__name__)
if iiens:
    app.config["JSON_SORT_KEYS"] = False
    app.config['MYSQL_HOST'] = 'mysql.iiens.net'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = mdp
    app.config['MYSQL_DB'] = 'e_mennessi2021'
else:
    app.config["JSON_SORT_KEYS"] = False
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'secf'


mysql = MySQL(app)

@app.route("/")
def hello_world():
    return  render_template("rr.html")

def parse_info(train,seat_info):
    return {
        "departure_station": train[1],
        "arrival_station": train[2],
        "date": str(train[3]),
        "heure": str(train[4]),
        "seat":{
            "first_class_seat": seat_info[2],
            "business_class_seat": seat_info[3],
            "standard_class_seat": seat_info[4],
            "total": seat_info[5]
        }
    }

@app.route("/all")
def get_all_train():
    all_train = defaultdict(None)
    cursor = mysql.connection.cursor()
    cursor.execute(''' 
    SELECT * FROM `train_info` WHERE 1
    ''')
    train_info = cursor.fetchall()
    for train in train_info:

        cursor.execute(''' 
        SELECT * FROM `seat_info` WHERE train_id = %s;
        ''' % train[0])

        seat_info = cursor.fetchall()[0]

        all_train[str(train[0])] = parse_info(train,seat_info)

    mysql.connection.commit()
    cursor.close()

    return jsonify(all_train)

@app.route("/id/<id>")
def get_train_by_id(id=None):
    the_train = defaultdict(None)
    cursor = mysql.connection.cursor()
    cursor.execute(''' 
    SELECT * FROM `train_info` WHERE id = %s
    ''',[id])
    train = cursor.fetchall()[0]
    cursor.execute(''' 
    SELECT * FROM `seat_info` WHERE train_id = %s
    ''',[train[0]])
    seat_info = cursor.fetchall()[0]

    mysql.connection.commit()
    cursor.close()
    the_train[train[0]] = parse_info(train,seat_info)
    return jsonify(the_train)

@app.route("/departure_station/<station>")
def get_train_by_id_departure_station(station=None):
    the_train = defaultdict(None)
    cursor = mysql.connection.cursor()
    cursor.execute(''' 
    SELECT * FROM `train_info` WHERE departure_station = %s
    ''',[station])
    train = cursor.fetchall()[0]
    cursor.execute(''' 
    SELECT * FROM `seat_info` WHERE train_id = %s
    ''',[train[0]])
    seat_info = cursor.fetchall()[0]

    mysql.connection.commit()
    cursor.close()
    the_train[train[0]] = parse_info(train,seat_info)
    return jsonify(the_train)

@app.route("/arrival_station/<station>")
def get_train_by_arrival_station(station=None):
    the_train = defaultdict(None)
    cursor = mysql.connection.cursor()
    cursor.execute(''' 
    SELECT * FROM `train_info` WHERE arrival_station = %s
    ''',[station])
    train = cursor.fetchall()[0]
    cursor.execute(''' 
    SELECT * FROM `seat_info` WHERE train_id = %s
    ''',[train[0]])
    seat_info = cursor.fetchall()[0]

    mysql.connection.commit()
    cursor.close()
    the_train[train[0]] = parse_info(train,seat_info)
    return jsonify(the_train)

@app.route("/date/<date>")
def get_train_by_date(date=None):
    the_train = defaultdict(None)
    cursor = mysql.connection.cursor()
    cursor.execute(''' 
    SELECT * FROM `train_info` WHERE date = %s;
    ''',[date])
    train = cursor.fetchall()[0]
    cursor.execute(''' 
    SELECT * FROM `seat_info` WHERE train_id = %s
    ''',[train[0]])
    seat_info = cursor.fetchall()[0]

    mysql.connection.commit()
    cursor.close()
    the_train[train[0]] = parse_info(train,seat_info)
    return jsonify(the_train)

@app.route("/time/<time>")
def get_train_by_time(time=None):
    the_train = defaultdict(None)
    cursor = mysql.connection.cursor()
    cursor.execute(''' 
    SELECT * FROM `train_info` WHERE time = %s
    ''',[time])
    train = cursor.fetchall()[0]
    cursor.execute(''' 
    SELECT * FROM `seat_info` WHERE train_id = %s
    ''',[train[0]])
    seat_info = cursor.fetchall()[0]

    mysql.connection.commit()
    cursor.close()
    the_train[train[0]] = parse_info(train,seat_info)
    return jsonify(the_train)



@app.route("/add/<train_id>/<departure_station>/<arrival_station>/<date>/<time>/<first_class_seat>/<business_class_seat>/<standard_class_seat>")
def add_train(train_id=None,departure_station=None,arrival_station=None,date=None,time=None,first_class_seat=None,business_class_seat=None,standard_class_seat=None):
    try:
        all_seats = int(first_class_seat)+int(business_class_seat)+int(standard_class_seat)
    except:
        return "Les nombres de sieges ont mal été renseignés"
    #Creating a connection cursor
    cursor = mysql.connection.cursor()
    
    #Executing SQL Statements
    cursor.execute(''' 
    INSERT INTO `train_info`
    (`id`, `departure_station`, `arrival_station`, `date`, `time`) 
    VALUES (%s,%s,%s,%s,%s)
    ''',(train_id,departure_station,arrival_station,date,time))
    cursor.execute(''' 
    INSERT INTO `seat_info` 
    (`train_id`, `first_class_seat`, `business_class_seat`, `standard_class_seat`, `all_seats`) 
    VALUES (%s,%s,%s,%s,%s); 
    ''',(train_id,first_class_seat,business_class_seat,standard_class_seat,all_seats))

    #Saving the Actions performed on the DB
    mysql.connection.commit()
    
    #Closing the cursor
    cursor.close()

    return "Train ajouté"