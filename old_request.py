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