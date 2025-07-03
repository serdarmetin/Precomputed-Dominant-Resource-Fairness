#!/usr/bin/env python
# coding: utf-8

def pdrf():
    global c_pdrf
    for i, demand in enumerate(d_pdrf[0]):
        u_pdrf[d_pdrf[1][i]] += demand * np.floor(rates[0][i] * cycleIterations)
        c_pdrf += demand * np.floor(rates[0][i] * cycleIterations)
        s_pdrf[d_pdrf[1][i]] += ds_pdrf[0][i] * np.floor(rates[0][i] * cycleIterations)

def drf():
    global c_drf
    while(1):
        i = np.argmin(s_drf)
        if (r < d_drf[i] + c_drf).any():
            break
        else:
            u_drf[i] += d_drf[i]
            s_drf[i] += ds_drf[0][i]
            c_drf += d_drf[i]

import numpy as np
import math
from numpy import random

numberOfUsers = 1000
numberOfResources = 10

r_low = 50000
r_high = 100001

#support = 5000
#spread = 1500

d_low = 1
d_high = 11

r = np.floor(np.random.randint(r_low, r_high, numberOfResources)) #resources
#r = np.ceil(spread * 10000 * np.random.standard_normal(numberOfResources) + support * 10000) #resources
c = np.zeros(numberOfResources) #consumed amounts
d = np.floor(np.random.randint(d_low, d_high, (numberOfUsers, numberOfResources))) #demand vector
#d = np.ceil(spread * np.random.standard_normal((numberOfUsers, numberOfResources)) + support) #demand vector

u_drf = np.zeros((numberOfUsers, numberOfResources)) #resources allocated to users
c_drf = np.zeros(numberOfResources) #resources allocated to users
s_drf = np.zeros(numberOfUsers) #allocated dominant shares of users
ds_drf = [(d / r).max(axis=1), np.expand_dims(np.arange(10), axis=1)]
d_drf = np.copy(d)

u_pdrf = np.zeros((numberOfUsers, numberOfResources)) #resources allocated to users
c_pdrf = np.zeros(numberOfResources) #resources allocated to users
s_pdrf = np.zeros(numberOfUsers) #allocated dominant shares of users
ds_pdrf = [(d / r).max(axis=1), np.expand_dims(np.arange(numberOfUsers), axis=1)]
d_pdrf = [d, np.expand_dims(np.arange(numberOfUsers), axis=1)]

s_max = np.max(ds_pdrf[0]) * np.ones(len(d_pdrf[0]))
rates = [s_max / ds_pdrf[0], np.expand_dims(np.arange(len(d_pdrf[0]),), axis=1)]

cycleDemands = np.sum(rates[0][:,np.newaxis] * d_pdrf[0], axis=0)
cycleIterations = np.min(r / cycleDemands)


drf()

pdrf()

difference = (u_drf - u_pdrf) / d

print(np.count_nonzero(difference == 1, axis=0)[0], np.count_nonzero(difference == 2, axis=0)[0], np.count_nonzero(difference > 2), int(difference.max(axis=0).max()), np.sum(difference > 0, axis=0)[0], np.count_nonzero(difference == -1, axis=0)[0], np.count_nonzero(difference == -2, axis=0)[0], np.count_nonzero(difference < -2, axis=0)[0], int(np.absolute(difference.min(axis=0).min())), np.sum(difference < 0, axis=0)[0])

#print(u_pdrf)
