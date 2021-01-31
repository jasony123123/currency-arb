import subprocess
import math
import requests
import json
import datetime
import pickle

class Bijection:
    def __init__(self):
        self.c12 = dict()
        self.c21 = dict()
        self.sz = 0
    def get12(self, one):
        return self.c12[one]
    def get21(self, two):
        return self.c21[two];
    def add1(self, one):
        if one not in self.c12:
            self.c12[one] = self.sz
            self.c21[self.sz] = one
            self.sz += 1

def calculate_arbitrage(data):
    nodeid = Bijection()
    edgeid = Bijection()
    edgeidTodata = dict()
    inputstr = ''
    retstr = ''

    for edge in data:
        edgeid.add1(edge[3])
        edgeidTodata[edgeid.get12(edge[3])] = edge
        nodeid.add1(edge[0])
        nodeid.add1(edge[1])
        inputstr += '{} {} {} {} '.format(nodeid.get12(edge[0]), nodeid.get12(edge[1]), -math.log(edge[2]), edgeid.get12(edge[3]))
    inputstr = '{} {} '.format(edgeid.sz, nodeid.sz) + inputstr

    sp = subprocess.run(args='make', capture_output=True, text=True, input=inputstr)
    res = sp.stdout.split('|')[1].split()
    if(res[0] == 'Yes'):
        retstr += 'Arbitrage Opp\n'
        gains = 1000000
        for i in range(1, len(res), 2):
            node = int(res[i])
            edge = int(res[i+1])
            retstr += '{}\t{}\t{}\t{}\n'.format(edgeidTodata[edge][0], edgeidTodata[edge][1], edgeidTodata[edge][2], edgeidTodata[edge][3])
            gains *= edgeidTodata[edge][2]
        retstr += '1000000 to {}\n'.format(gains)
    else:
        retstr += 'No Arbitrage Opps\n'
    return retstr

def get_data():
    url = 'https://api.exchangeratesapi.io/latest?base='
    edges = []
    abbr = ['CAD', 'HKD', 'ISK', 'PHP', 'DKK', 'HUF', 'CZK', 'GBP', 'RON', 'SEK', 'IDR', 'INR', 'BRL', 'RUB', 'HRK', 'JPY', 'THB', 'CHF', 'EUR', 'MYR', 'BGN', 'TRY', 'CNY', 'NOK', 'NZD', 'ZAR', 'USD', 'MXN', 'SGD', 'AUD', 'ILS', 'KRW', 'PLN']
    time = str(datetime.datetime.now()).replace(' ', '-').split('.')[0]
    for base in abbr:
        print('requesting', base)
        r = json.loads(requests.get(url + base).text)
        print('loaded and parsed w no problems')
        for to, rate in r['rates'].items():
            if to != base:
                id = 'id.{}.{}.exchangeratesapi.{}'.format(base, to, time)
                edges.append([base, to, rate, id])
    return edges

def run_arbitrage():
    ret = ''
    try:
        with open('data.pickle', 'rb') as handle:
            d = pickle.load(handle)
    except Exception as e:
        ret += 'Error loading data, using backup\n' + str(e)

    if(len(ret) > 1):
        with open('data_backup.pickle', 'rb') as handle:
            d = pickle.load(handle)

    try:
        answer = calculate_arbitrage(d)
    except Exception as e:
        ret += '\nError calculating'
        return ret

    return ret + '\n' + answer

def update_data():
    try:
        data = get_data()
        with open('data.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return 'Success'
    except Exception as e:
        return 'Fail' + str(e)

print(run_arbitrage())
