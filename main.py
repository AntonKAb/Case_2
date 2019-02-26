"""
Case 2
Developers: Kabaev A., Anufrienko K., Lankevich S.
"""
import random


def file_reading():
    petrol_stations = dict()
    clients = dict()
    with open('azs.txt') as petrols_file:
        data = petrols_file.readlines()
        for petrol in data:
            petrol_data = petrol.rstrip().split()
            petrol_stations.update({int(petrol_data[0]) - 1: {'cars_number': int(petrol_data[1]),
                                                              'oil': [], 'queue': []}})
            for oil in petrol_data[2:]:
                petrol_stations[int(petrol_data[0]) - 1]['oil'].append(oil)
            for _ in range(petrol_stations[int(petrol_data[0]) - 1]['cars_number']):
                petrol_stations[int(petrol_data[0]) - 1]['queue'].append(0)
    with open('input.txt') as clients_file:
        data = clients_file.readlines()
        number = 0
        for client in data:
            client_data = client.rstrip().split()
            clients.update({number: {'arrival': client_data[0], 'value': int(client_data[1]),
                                     'oil': client_data[2], 'action': False, 'away': None, 'time': None}})
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
    random_time = random.choice([-1, 0, 1])
    if int(time_new) % 10:
        return int(time_new / 10) + 2 + random_time
    else:
        if int(time_new / 10) + 1 == 1:
            return int(time_new / 10) + 1
        return int(time_new / 10) + 1 + random_time


def crowd():
    azs = file_reading()['petrol_stations']
    client_base = file_reading()['clients']
    print(azs)
    time = time_list()
    time_azs_status = dict()
    client_event_list = dict()
    statistic = {'oil': {'АИ-80': 0, 'АИ-92': 0, 'АИ-95': 0, 'АИ-98': 0}, 'sum': 0, 'turned_clients': 0}
    for current_time in time:
        client_event_list.update({current_time: []})
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
                    client_base[number]['action'] = azs_min + 1
                    client_base[number]['time'] = time_counting(client_base[number]['value'])
                    if queue_min == 0:
                        azs_copy[azs_min]['queue'][queue_min] = client_base[number]['time']
                    else:
                        azs_copy[azs_min]['queue'][queue_min] = azs_copy[azs_min]['queue'][queue_min - 1] + \
                                                                client_base[number]['time']
                    client_event_list[part].append({'action': 'arrival', 'id': number})
                    time_index = time.index(part) + client_base[number]['time']
                    if time_index > len(time):
                        time_index -= len(time)
                        client_event_list[time[time_index]].append({'action': 'next_day_away', 'id': number})
                    else:
                        client_event_list[time[time_index]].append({'action': 'away', 'id': number})
                    statistic['oil'][client_base[number]['oil']] += client_base[number]['time']
                    statistic['sum'] += client_base[number]['time']
                for el in stations_free:
                    if client_base[number]['oil'] != azs[el]['oil'] and len(stations_free) == 1:
                        client_event_list[part].append({'action': 'no_fueling', 'id': number})
                        statistic["turned_clients"] += 1
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
    return {'clients': client_base, 'day_protocol': time_azs_status,
            'client_event_list': client_event_list, 'stat': statistic}


def print_stat(azs):
    for petrol in azs:
        current_petrol = azs[petrol]
        message = 'Автомат №{}  максимальная очередь: {} Марки бензина: {} ->{} '
        oil_list = current_petrol['oil']
        oil_text = ''
        for oil in oil_list:
            oil_text += f'{oil}, '
        oil_text = oil_text[:-2]
        try:
            print(message.format(petrol + 1, current_petrol['cars_number'],
                                 oil_text, '*' * (current_petrol['queue'].index(0))))
        except ValueError:
            print(message.format(petrol + 1, current_petrol['cars_number'],
                                 oil_text, '*' * current_petrol['cars_number']))


def main():
    day_on_petrol = crowd()
    clients = day_on_petrol['clients']
    day_protocol = day_on_petrol['day_protocol']
    client_events_list = day_on_petrol['client_event_list']
    statistic = day_on_petrol['stat']
    print(statistic)
    for time in client_events_list:
        for event in client_events_list[time]:
            action = event['action']
            client_id = event['id']
            client = clients[client_id]
            if action == 'arrival':
                message = 'В  {}  новый клиент:  {} {} {} {} встал в очередь к автомату №{} '
                print(message.format(time, time,
                                     client["oil"], client["value"],
                                     client["time"],
                                     client["action"]))
                print_stat(day_protocol[time])
            elif action == 'away':
                message = 'В  {}  клиент  {} {} {} {}  заправил свой автомобиль и покинул АЗС.'
                print(message.format(time, client['arrival'], client["oil"], client["value"], client['time']))
                print_stat(day_protocol[time])
            elif action == 'no_fueling':
                message = 'В  {}  новый клиент:  {} {} {} {} не смог заправить автомобиль и покинул АЗС. '
                print(message.format(time, time, client["oil"], client["value"], client['time']))
                print_stat(day_protocol[time])
    for time in client_events_list:
        for event in client_events_list[time]:
            action = event['action']
            client_id = event['id']
            client = clients[client_id]
            if action == 'next_day_away':
                message = 'В  {}  клиент  {} {} {} {}  заправил свой автомобиль и покинул АЗС.'
                print(message.format(time, client['arrival'], client["oil"], client["value"], client['time']))
                print_stat(day_protocol[time])
    print(f'За сутки было продано {statistic["oil"]["АИ-80"]} литров АИ-80, \
{statistic["oil"]["АИ-92"]} литров АИ-92, \n{" "* len("За сутки было продано ")}{statistic["oil"]["АИ-95"]}\
 литров АИ-95, {statistic["oil"]["АИ-98"]} литров АИ-98\nИтого: {statistic["sum"]}\n\
С заправки уехало {statistic["turned_clients"]} клиентов')


main()
