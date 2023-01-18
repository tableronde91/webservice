from suds.client import Client
from prettytable import PrettyTable
import json
import ast

hello_client = Client('http://localhost:7789/?wsdl')

while(True):
    print("1. Get all trains")
    print("2. Reserve outbound")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        string_data = str(hello_client.service.get_all_trains()[0][0])
        dict_data = ast.literal_eval(string_data)

        chaine = "ID | Departure Station | Arrival Station | Departure Date | Departure Time | First Class Seat | Business Class Seat | Standard Seats | Total Seats \n"
        for id,val in dict_data.items():
            chaine =chaine + str(id) + " | " +str(val["departure_station"])+ " | "+str(val["arrival_station"])+" | " + str(val["departure_date"]) + " | " + str(val["departure_time"])+ " | " + str(val["seat"]["first_class_seat"])+ " | " +str(val["seat"]["business_class_seat"])+ " | " +str(val["seat"]["standard_class_seat"])+ " | " + str(val["seat"]["total"])+"\n"
        print(chaine)
    elif choice == 2:
        train_id = int(input("Enter train id: "))
        classe = input("Enter classe: ")
        places = int(input("Enter number of places: "))
        print(hello_client.service.reserve_outbound(train_id,classe,places))
    elif choice == 3:
        break
    else:
        print("Invalid choice")