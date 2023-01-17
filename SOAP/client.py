from suds.client import Client
from beautifultable import BeautifulTable
import json
import ast

hello_client = Client('http://localhost:7789/?wsdl')

while(True):
    print("1. Get all trains")
    print("2. Reserve outbound")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        print(hello_client.service.get_all_trains())
    elif choice == 2:
        train_id = int(input("Enter train id: "))
        classe = input("Enter classe: ")
        places = int(input("Enter number of places: "))
        print(hello_client.service.reserve_outbound(train_id,classe,places))
    elif choice == 3:
        break
    else:
        print("Invalid choice")