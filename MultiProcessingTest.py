# -*- coding: utf-8 -*-
"""
Created on Thu May 04 12:54:49 2017

@author: ehill
"""

import multiprocessing as mp
import time
import random


def task(num, lock):
    lock.acquire()
    print '\nTask ' + str(num) + ' starting...'
    lock.release()
#    time.sleep(5)
    for i in range(int(5E6)):
        j = random.random()*random.random()
    lock.acquire()
    print '\nTask ' + str(num) + ' complete.'
    lock.release()
    

if __name__ == '__main__':
    lock = mp.Lock()
    for i in range(20):
        t = mp.Process(target=task, args=(i,lock))
        t.start()
        


    time.sleep(10)



