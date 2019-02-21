"""
Case 2
Developers: Kabaev A., Anufrienko K., Lankevich S.
"""


def file_reading():
    petrol_stations = dict()
    clients = dict()
    with open('azs.txt') as petrols_file:
        data = petrols_file.readlines()
        for petrol in data:
            petrol_data = petrol.rstrip().split()
            petrol_stations.update({int(petrol_data[0])-1: {'cars_number': int(petrol_data[1]), 'oil': []}})
            for oil in petrol_data[2:]:
                petrol_stations[int(petrol_data[0])-1]['oil'].append(oil)
    with open('input.txt') as clients_file:
        data = clients_file.readlines()
        number = 0
        for client in data:
            client_data = client.rstrip().split()
            clients.update({number: {'arrival': client_data[0], 'time': int(client_data[1]), 'oil': client_data[2]}})
            number += 1
    return {'petrol_stations': petrol_stations, 'clients': clients}


print(file_reading()['clients'])
