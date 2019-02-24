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


def time_counting(time_new):
    if int(time_new) % 10:
        return int(time_new / 10) + 2
    else:
        return int(time_new / 10) + 1


def crowd():
    azs = file_reading()['petrol_stations']
    client_base = file_reading()['clients']
    time = time_list()[1:]
    time_azs_status = dict()
    for part in time:
        azs_copy = dict()
        for el in azs:
            el_copy = azs[el].copy()
            el_copy['queue'] = azs[el]['queue'].copy()
            azs_copy.update({el: el_copy})
        for number in range(len(client_base)):
            if part == client_base[number]['arrival']:
                stations = []
                for azs_d in range(len(azs_copy)):
                    if client_base[number]['oil'] in azs_copy[azs_d]['oil']:
                        stations.append(azs_d)
                stations_free = []
                for free in stations:
                    if azs_copy[free]['queue'][-1] == 0:
                        stations_free.append(free)
                if len(stations_free):
                    queue_min = float('inf')
                    azs_min = None
                    for i in stations_free:
                        if azs_copy[i]['queue'].index(0) < queue_min:
                            queue_min = azs_copy[i]['queue'].index(0)
                            azs_min = i
                    client_base[number]['action'] = azs_min
                    if queue_min == 0:
                        azs_copy[azs_min]['queue'][queue_min] = time_counting(client_base[number]['time'])
                    else:
                        azs_copy[azs_min]['queue'][queue_min] = azs_copy[azs_min]['queue'][queue_min - 1] +\
                                                           time_counting(client_base[number]['time'])
        azs = azs_copy
        time_azs_status.update({part: azs})
        for i in azs.keys():
            for x in range(len(azs[i]['queue'])):
                if azs[i]['queue'][x]:
                    azs[i]['queue'][x] -= 1
            for _ in azs[i]['queue']:
                if not azs[i]['queue'][0]:
                    azs[i]['queue'].pop(0)
                    azs[i]['queue'].append(0)
    return {'clients': client_base, 'day_protocol': time_azs_status}
