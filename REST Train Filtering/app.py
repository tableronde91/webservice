# --- Imports Part ---

from collections import defaultdict
import logging
from flask import Flask,render_template, request,jsonify, abort
from flask_mysqldb import MySQL

# --- Config Part ---

# with open("./db.mdp") as file:
#     mdp = file.read()
iiens = False

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
    return  render_template("doc.html")

# --- Data parsing Part ---

def parse_info(train,seat_info):
    return {
        "departure_station": train[1],
        "arrival_station": train[2],
        "departure_date": str(train[3]),
        "departure_time": str(train[4]),
        "flex": str(train[5]),
        "price": str(train[6]),
        "seat":{
            "first_class_seat": seat_info[2],
            "business_class_seat": seat_info[3],
            "standard_class_seat": seat_info[4],
            "total": seat_info[5]
        }
    }

def data_to_string(datas,absolute_str=True):
    string = "("
    for i,data in enumerate(datas):
        if absolute_str:
            string += "'"+(data)+"'"
        else:
            string += data
        if i < len(datas)-1:
            string += ","
    string += ")"
    return string

def check_data(departure_station=" ",arrival_station=" ",departure_date=" ",departure_time=" "):
    datas = []
    items = []
    if departure_station != " ":
        datas.append(str(departure_station))
        items.append("departure_station")
    if arrival_station != " ":
        datas.append(str(arrival_station))
        items.append("arrival_station")
    if departure_date != " ":
        datas.append(str(departure_date))
        items.append("departure_date")
    if departure_time != " ":
        datas.append(str(departure_time))
        items.append("departure_time")
    return datas,items

# --- Filter Part ---

def filter_request(string_items,string_datas,classe=None,nb_ticket=None):
    all_train = defaultdict(None)
    cursor = mysql.connection.cursor()
    cursor.execute(''' 
        SELECT * FROM `train_info` WHERE {} = {}
        '''.format(string_items,string_datas))
    train_info = cursor.fetchall()
    for train in train_info:
        cursor.execute(''' 
        SELECT * FROM `seat_info` WHERE train_id = {}
        '''.format(train[0]))

        seat_info = cursor.fetchall()[0]
        if classe != None and nb_ticket != None:
            if classe == "premiere" and seat_info[2] >= int(nb_ticket):
                all_train[str(train[0])] = parse_info(train,seat_info)
            elif classe == "affaire" and seat_info[3] >= int(nb_ticket):
                all_train[str(train[0])] = parse_info(train,seat_info)
            elif classe == "standard" and seat_info[4] >= int(nb_ticket):
                all_train[str(train[0])] = parse_info(train,seat_info)
        else:
            all_train[str(train[0])] = parse_info(train,seat_info)

    return all_train

def filter_return_request(string_items,string_datas,string_return_items,string_return_datas,classe=None,nb_ticket=None):
    all_train = defaultdict(None)

    cursor = mysql.connection.cursor()
    cursor.execute(''' 
        SELECT * FROM `train_info` WHERE {} = {}
        '''.format(string_items,string_datas))
    train_info = cursor.fetchall()

    for train in train_info:
        cursor.execute(''' 
        SELECT * FROM `seat_info` WHERE train_id = {}
        '''.format(train[0]))

        seat_info = cursor.fetchall()[0]

        if classe != None and nb_ticket != None:
            if classe == "premiere" and seat_info[2] >= int(nb_ticket):
                all_train[str(train[0])] = parse_info(train,seat_info)
            elif classe == "affaire" and seat_info[3] >= int(nb_ticket):
                all_train[str(train[0])] = parse_info(train,seat_info)
            elif classe == "standard" and seat_info[4] >= int(nb_ticket):
                all_train[str(train[0])] = parse_info(train,seat_info)
            else:
                continue
        else:
            all_train[str(train[0])] = parse_info(train,seat_info)
    
        cursor.execute('''
            SELECT * FROM `train_info` WHERE {} = {}
            '''.format(string_return_items,string_return_datas))
        train_return_info = cursor.fetchall()

        all_train[str(train[0])]["return"] = defaultdict(None)
        for train_return in train_return_info:
            cursor.execute(''' 
            SELECT * FROM `seat_info` WHERE train_id = {}
            '''.format(train_return[0]))

            seat_return_info = cursor.fetchall()[0]
            if classe != None and nb_ticket != None:
                if classe == "premiere" and seat_return_info[2] >= int(nb_ticket):
                    all_train[str(train[0])]["return"][str(train_return[0])] = parse_info(train_return,seat_return_info)
                elif classe == "affaire" and seat_return_info[3] >= int(nb_ticket):
                    all_train[str(train[0])]["return"][str(train_return[0])] = parse_info(train_return,seat_return_info)
                elif classe == "standard" and seat_return_info[4] >= int(nb_ticket):
                    all_train[str(train[0])]["return"][str(train_return[0])] = parse_info(train_return,seat_return_info)
            else:
                all_train[str(train[0])]["return"][str(train_return[0])] = parse_info(train_return,seat_return_info)

    return all_train

# --- Filtre train depart seulement ---

@app.route("/trains")
def get_all_train():
    all_train = defaultdict(None)
    cursor = mysql.connection.cursor()
    cursor.execute(''' 
    SELECT * FROM `train_info` WHERE 1
    ''')
    train_info = cursor.fetchall()
    for train in train_info:
        cursor.execute(''' 
            SELECT * FROM `seat_info` WHERE train_id = {}
            '''.format(train[0]))
        seat_info = cursor.fetchall()[0]
        all_train[str(train[0])] = parse_info(train,seat_info)
    mysql.connection.commit()
    cursor.close()
    return jsonify(all_train)

@app.route("/train/depart/<departure_station>")
def get_train_depart(departure_station):
    datas, items = check_data(departure_station)
    if len(datas) < 1:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/classe/<classe>/places/<nb_ticket>")
def get_train_depart_classe(departure_station,classe,nb_ticket):
    datas, items = check_data(departure_station)
    if len(datas) < 1:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas,classe,nb_ticket)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/date/<departure_date>")
def get_train_depart_date(departure_station,departure_date):
    datas, items = check_data(departure_station,departure_date=departure_date)
    if len(datas) < 2:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/date/<departure_date>/classe/<classe>/places/<nb_ticket>")
def get_train_depart_date_classe(departure_station,departure_date,classe,nb_ticket):
    datas, items = check_data(departure_station,departure_date=departure_date)
    if len(datas) < 2:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas,classe,nb_ticket)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/date/<departure_date>/heure/<departure_time>")
def get_train_depart_date_heure(departure_station,departure_date,departure_time):
    datas, items = check_data(departure_station,departure_date=departure_date,departure_time=departure_time)
    if len(datas) < 3:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/date/<departure_date>/heure/<departure_time>/classe/<classe>/places/<nb_ticket>")
def get_train_depart_date_heure_classe(departure_station,departure_date,departure_time,classe,nb_ticket):
    datas, items = check_data(departure_station,departure_date=departure_date,departure_time=departure_time)
    if len(datas) < 3:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas,classe,nb_ticket)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

# --- Filtre train depart et arrive ---

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>")
def get_train_depart_arrive(departure_station,arrival_station):
    datas, items = check_data(departure_station,arrival_station=arrival_station)
    if len(datas) < 2:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/classe/<classe>/places/<nb_ticket>")
def get_train_depart_arrive_classe(departure_station,arrival_station,classe,nb_ticket):
    datas, items = check_data(departure_station,arrival_station=arrival_station)
    if len(datas) < 2:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas,classe,nb_ticket)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/date/<departure_date>")
def get_train_depart_arrive_date(departure_station,arrival_station,departure_date):
    datas, items = check_data(departure_station,arrival_station=arrival_station,departure_date=departure_date)
    if len(datas) < 3:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/date/<departure_date>/classe/<classe>/places/<nb_ticket>")
def get_train_depart_arrive_date_classe(departure_station,arrival_station,departure_date,classe,nb_ticket):
    datas, items = check_data(departure_station,arrival_station=arrival_station,departure_date=departure_date)
    if len(datas) < 3:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas,classe,nb_ticket)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/date/<departure_date>/heure/<departure_time>")
def get_train_depart_arrive_date_heure(departure_station,arrival_station,departure_date,departure_time):
    datas, items = check_data(departure_station,arrival_station=arrival_station,departure_date=departure_date,departure_time=departure_time)
    if len(datas) < 4:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/date/<departure_date>/heure/<departure_time>/classe/<classe>/places/<nb_ticket>")
def get_train_depart_arrive_date_heure_classe(departure_station,arrival_station,departure_date,departure_time,classe,nb_ticket):
    datas, items = check_data(departure_station,arrival_station=arrival_station,departure_date=departure_date,departure_time=departure_time)
    if len(datas) < 4:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)

    all_train = filter_request(string_items,string_datas,classe,nb_ticket)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

# --- Filtre avec trains (depart et arrive) aller et retour ---

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/retour")
def get_train_depart_arrive_retour(departure_station,arrival_station):
    datas, items = check_data(departure_station,arrival_station=arrival_station)
    return_data, return_items = check_data(departure_station=arrival_station,arrival_station=departure_station)
    if len(datas) < 2 or len(return_data) < 2:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)
    string_return_datas = data_to_string(return_data)
    string_return_items = data_to_string(return_items,False)

    all_train = filter_return_request(string_items,string_datas,string_return_items,string_return_datas)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/retour/classe/<classe>/places/<nb_ticket>")
def get_train_depart_arrive_retour_classe(departure_station,arrival_station,classe,nb_ticket):
    datas, items = check_data(departure_station,arrival_station=arrival_station)
    return_data, return_items = check_data(departure_station=arrival_station,arrival_station=departure_station)
    if len(datas) < 2 or len(return_data) < 2:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)
    string_return_datas = data_to_string(return_data)
    string_return_items = data_to_string(return_items,False)

    all_train = filter_return_request(string_items,string_datas,string_return_items,string_return_datas,classe,nb_ticket)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/date/<departure_date>/retour/date/<return_date>")
def get_train_depart_arrive_date_retour_date(departure_station,arrival_station,departure_date,return_date):
    datas, items = check_data(departure_station,arrival_station=arrival_station,departure_date=departure_date)
    return_data, return_items = check_data(departure_station=arrival_station,arrival_station=departure_station,departure_date=return_date)
    if len(datas) < 3 or len(return_data) < 3:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)
    string_return_datas = data_to_string(return_data)
    string_return_items = data_to_string(return_items,False)

    all_train = filter_return_request(string_items,string_datas,string_return_items,string_return_datas)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/date/<departure_date>/retour/date/<return_date>/classe/<classe>/places/<nb_ticket>")
def get_train_depart_arrive_date_retour_date_classe(departure_station,arrival_station,departure_date,return_date,classe,nb_ticket):
    datas, items = check_data(departure_station,arrival_station=arrival_station,departure_date=departure_date)
    return_data, return_items = check_data(departure_station=arrival_station,arrival_station=departure_station,departure_date=return_date)
    if len(datas) < 3 or len(return_data) < 3:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)
    string_return_datas = data_to_string(return_data)
    string_return_items = data_to_string(return_items,False)

    all_train = filter_return_request(string_items,string_datas,string_return_items,string_return_datas,classe,nb_ticket)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/date/<departure_date>/heure/<departure_time>/retour/date/<return_date>/heure/<return_time>")
def get_train_depart_arrive_date_heure_retour_date_heure(departure_station,arrival_station,departure_date,departure_time,return_date,return_time):
    datas, items = check_data(departure_station,arrival_station=arrival_station,departure_date=departure_date,departure_time=departure_time)
    return_data, return_items = check_data(departure_station=arrival_station,arrival_station=departure_station,departure_date=return_date,departure_time=return_time)
    if len(datas) < 4 or len(return_data) < 4:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)
    string_return_datas = data_to_string(return_data)
    string_return_items = data_to_string(return_items,False)

    all_train = filter_return_request(string_items,string_datas,string_return_items,string_return_datas)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

@app.route("/train/depart/<departure_station>/arrive/<arrival_station>/date/<departure_date>/heure/<departure_time>/retour/date/<return_date>/heure/<return_time>/classe/<classe>/places/<nb_ticket>")
def get_train_depart_arrive_date_heure_retour_date_heure_classe(departure_station,arrival_station,departure_date,departure_time,return_date,return_time,classe,nb_ticket):
    datas, items = check_data(departure_station,arrival_station=arrival_station,departure_date=departure_date,departure_time=departure_time)
    return_data, return_items = check_data(departure_station=arrival_station,arrival_station=departure_station,departure_date=return_date,departure_time=return_time)
    if len(datas) < 4 or len(return_data) < 4:
        abort(400, "Données incorrectes")

    string_datas = data_to_string(datas)
    string_items = data_to_string(items,False)
    string_return_datas = data_to_string(return_data)
    string_return_items = data_to_string(return_items,False)

    all_train = filter_return_request(string_items,string_datas,string_return_items,string_return_datas,classe,nb_ticket)

    if len(all_train) < 1:
        abort(404, "Aucun train disponible")
    else:
        return jsonify(all_train)

# --- Update part ---

def reservation_request(train_id,classe,nb_ticket):
    cursor = mysql.connection.cursor()
    cursor.execute(''' 
        SELECT * FROM `seat_info` WHERE train_id = {}
        '''.format(train_id))

    seat_info = cursor.fetchall()[0]
    
    if classe == "premiere":
        if seat_info[2] >= int(nb_ticket):
            cursor.execute('''
                UPDATE `seat_info` SET `first_class_seat` = `first_class_seat` - {}, `all_seats` = `all_seats` - {} WHERE `seat_info`.`train_id` = {}
                '''.format(nb_ticket,nb_ticket,train_id))
            mysql.connection.commit()
            return True
        else:
            raise Exception("Reservation impossible, nombre de place insuffisant en {} classe".format(classe))
    elif classe == "affaire":
        if seat_info[3] >= int(nb_ticket):
            cursor.execute(''' 
                UPDATE `seat_info` SET `business_class_seat` = `business_class_seat` - {}, `all_seats` = `all_seats` - {} WHERE `seat_info`.`train_id` = {}
                '''.format(nb_ticket,nb_ticket,train_id))
            mysql.connection.commit()
            return True
        else:
            raise Exception("Reservation impossible, nombre de place insuffisant en classe {}".format(classe))
        
    elif classe == "standard":
        if seat_info[4] >= int(nb_ticket):
            cursor.execute('''
                UPDATE `seat_info` SET `standard_class_seat` = `standard_class_seat` - {}, `all_seats` = `all_seats` - {} WHERE `seat_info`.`train_id` = {}
                '''.format(nb_ticket,nb_ticket,train_id))
            mysql.connection.commit()
            return True
        else:
            raise Exception("Reservation impossible, nombre de place insuffisant en classe {}".format(classe))
    else:
        raise Exception("Reservation impossible, classe : {} incorrect".format(classe))

@app.route("/revervation/train/<train_id>",methods=["PUT"])
def update_reservation(train_id):
    data = request.get_json()
    classe = data["classe"]
    nb_ticket = data["nb_ticket"]

    if classe != "premiere" and classe != "affaire" and classe != "standard":
        abort(400,"Reservation impossible, classe : {} incorrect".format(classe))
    if int(nb_ticket) < 1:
        abort(400,"Reservation impossible, nombre de place : {} incorrect".format(nb_ticket))
    
    try:
        if reservation_request(train_id,classe,nb_ticket):
            return jsonify("Reservation effectuée")
        else:
            abort(400,"Reservation impossible")
    except IndexError as e:
        abort(400,"Reservation impossible, train : {} indisponible".format(train_id))
    except Exception as e:
        abort(400,e.args[0] + " | train : {} (train aller)".format(train_id))

@app.route("/revervation/train/<train_id>/retour/train/<return_train_id>",methods=["PUT"])
def update_reservation_return(train_id,return_train_id):
    data = request.get_json()
    classe = data["classe"]
    nb_ticket = data["nb_ticket"]

    if classe != "premiere" and classe != "affaire" and classe != "standard":
        abort(400,"Reservation impossible, classe : {} incorrect".format(classe))
    if int(nb_ticket) < 1:
        abort(400,"Reservation impossible, nombre de place : {} incorrect".format(nb_ticket))
    try:
        if reservation_request(train_id,classe,nb_ticket):
            try:
                if reservation_request(return_train_id,classe,nb_ticket):
                    return jsonify("Reservation effectuée")
                else:
                    abort(400,"Reservation impossible")
            except IndexError as e:
                abort(400,"Reservation impossible, train de retour : {} indisponible".format(return_train_id))
            except Exception as e:
               abort(400,e.args[0] + " | train : {} (train retour)".format(return_train_id))
        else:
            abort(400,"Reservation impossible")
    except IndexError as e:
        abort(400,"Reservation impossible, train : {} indisponible".format(train_id))
    except Exception as e:
        abort(400,e.args[0] + " | train : {} (train aller)".format(train_id))

