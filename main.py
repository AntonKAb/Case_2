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
            petrol_stations.update({int(petrol_data[0])-1: {'cars_number': int(petrol_data[1]),
                                                            'oil': [], 'queue': []}})
            for oil in petrol_data[2:]:
                petrol_stations[int(petrol_data[0])-1]['oil'].append(oil)
            for _ in range(petrol_stations[int(petrol_data[0])-1]['cars_number']):
                petrol_stations[int(petrol_data[0]) - 1]['queue'].append(0)
    with open('input.txt') as clients_file:
        data = clients_file.readlines()
        number = 0
        for client in data:
            client_data = client.rstrip().split()
            clients.update({number: {'arrival': client_data[0], 'time': int(client_data[1]),
                                     'oil': client_data[2], 'action': False}})
            number += 1
    return {'petrol_stations': petrol_stations, 'clients': clients}


def time_list():
    day_time_list = []
    for hour in range(24):
        for minute in range(60):
            current_hour = str(hour).rjust(2, '0')
            current_minute = str(minute).rjust(2, '0')
            day_time_list.append(f'{current_hour}:{current_minute}')
    return day_time_list
