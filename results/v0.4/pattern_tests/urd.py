from typing import Dict
from enum import Enum
import pandas as pd
import numpy as np
from scipy import stats

class IoType(Enum):
    read = 0
    write = 1

class UrdObject(object):
    def __init__(self):
        self.__map = dict()  # type: Dict[int, bool]
        self.__frequency = 0
        self.__max_count = -1
        self.__average_urd = 0
        self.__urd_count = 0

    def add(self, address):
        self.__map[address] = True

    def get_max_count(self):
        return self.__max_count

    def get_frequency(self):
        return self.__frequency

    def get_average(self):
        return self.__average_urd

    def get_count(self):
        return self.__urd_count

    def initialize_next(self):
        if len(self.__map) == 0:
            return
        if self.__max_count < len(self.__map):
            self.__max_count = len(self.__map)
            self.__frequency = 1
        elif self.__max_count == len(self.__map):
            self.__frequency += 1
        self.__average_urd = (self.__average_urd * self.__urd_count + len(self.__map)) / (self.__urd_count + 1)
        self.__urd_count += 1
        self.__map.clear()

    def reset_urd(self):
        self.__map.clear()

class Urd(object):
    def __init__(self):
        self.urd_object = dict()  # type: Dict[int, UrdObject]

    def access(self, address, io_type):
        try:
            urd_object = self.urd_object[address]
        except KeyError:
            self.urd_object[address] = UrdObject()
            return
        finally:
            for key, value in self.urd_object.items():
                if key != address:
                    value.add(address)

        if io_type == IoType.write:
            urd_object.reset_urd()
            return

        self.urd_object[address].initialize_next()

    def finish(self):
        for key, value in self.urd_object.items():
            value.initialize_next()

    def print_data(self):
        for key, value in sorted(self.urd_object.items()):
            print("%s: avg: %s, count: %s" % (key, value.get_average(), value.get_count()))

    def get_data(self):
        columns = ['avg', 'count']
        data = np.zeros(shape=(len(self.urd_object.items()),2))
        addr = np.zeros(shape=(len(self.urd_object.items())), dtype='int')
        i = 0
        for key, value in sorted(self.urd_object.items()):
            addr[i] = key
            data[i,0] = value.get_average()
            data[i,1] = value.get_count()
            i = i+1
        df = pd.DataFrame(data, columns=columns)
        df['addr'] = addr
        df['count'] = df['count'] + 1
        df['weight'] = df['count'] / np.sum((df['count']))
        return df

def process(trace):
    urd_instance = Urd()

    for t in trace:
        urd_instance.access(t, IoType.read)

    return urd_instance.get_data()

def gen_and_process(pat):
    index, delta, length = pat
    trace = [0] * len(index)*length
    n = len(index)
    for i in range(length):
        for j in range(n):
            trace[i*n + j] = index[j] + delta*i

    return process(trace)

def get_mean(df):
    #df = df[df['avg'] != 0]
    return np.mean(df['avg']*df['weight'])

def thats_just_mean(pat):
    return get_mean(gen_and_process(pat))
#thats_just_mean = np.vectorize(thats_just_mean)



#df = gen_and_process(([*range(0,100)],1,20))
#print(get_mean(df))

