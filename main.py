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
            petrol_stations.update({petrol_data[0]: {'cars_number': petrol_data[1], 'oil': []}})
            for oil in petrol_data[2:]:
                petrol_stations[petrol_data[0]]['oil'].append(oil)
    with open('input.txt') as clients_file:
        data = clients_file.readlines()
        number = 0
        for client in data:
            client_data = client.rstrip().split()
            clients.update({number: {'arrival': client_data[0], 'time': client_data[1], 'oil': client_data[2]}})
            number += 1
    return {'petrol_stations': petrol_stations, 'clients': clients}