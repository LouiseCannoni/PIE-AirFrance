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


#Création de la date départ prévue DDP
dateetheure=vols['Date départ prévue TU']+vols['Heure départ prévue TU']
vols = vols.assign(DDP=pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M'))

#Création de la date départ réalisée DDR
dateetheure=vols['Date départ réalisée TU']+vols['Heure départ réalisée TU']
vols = vols.assign(DDR=pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M'))

#Création de la date arrivée prévue DAP
dateetheure=vols['Date arrivée prévue TU']+vols['Heure arrivée prévue TU']
vols = vols.assign(DAP=pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M'))

#Création de la date départ prévue DAR
dateetheure=vols['Date arrivée réalisée TU']+vols['Heure arrivée réalisée TU']
vols = vols.assign(DAR=pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M'))


#Calcul de retard au départ en minutes : Retard_D
Duree = vols.DDR - vols.DDP
vols = vols.assign(Retard_D = Duree.apply(lambda x: x.total_seconds()/60))

#Calcul de retard à l'arrivée en minutes : Retard_A
Duree = vols.DAR - vols.DAP
vols = vols.assign(Retard_A = Duree.apply(lambda x: x.total_seconds()/60))

#Filtrage sur les vols Air France et les avions moyen courrier : A320 family

vols_MC = vols[vols['Type exploitation']=='Air France']
vols_MC = vols_MC[vols_MC['Type avion réalisé'].apply(lambda x: (x=='318' or x=='319' or x=='320' or x=='321'))]
print(vols_MC)