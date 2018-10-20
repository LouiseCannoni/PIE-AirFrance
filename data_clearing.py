#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 17:58:41 2018

@author: louisecannoni
"""

import pandas
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from math import isnan

vols=pandas.read_csv("../Extract_1cut.csv",sep=',',decimal=b',')
vols['Date départ prévue TU'] = vols['Date départ prévue TU'].apply(lambda x: x[:10])
vols['Date départ réalisée TU'] = vols['Date départ réalisée TU'].apply(lambda x: x[:10])
vols['Date arrivée prévue TU'] = vols['Date arrivée prévue TU'].apply(lambda x: x[:10])
vols['Date arrivée réalisée TU'] = vols['Date arrivée réalisée TU'].apply(lambda x: x[:10])

print(vols.head)