from suds.client import Client
import json
import ast

hello_client = Client('http://localhost:7789/?wsdl')
string_data = str(hello_client.service.get_all_trains()[0][0])
dict_data = ast.literal_eval(string_data)
print(dict_data["departure_station"])
# print(dict_data)