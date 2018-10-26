#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 17:58:41 2018

@author: Malmonta
"""

import pandas
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from math import isnan

vols = pandas.read_csv("./Data/Extract_1cut.csv",sep=',',decimal=b',')

def data_cleaning(vols):
    
     #Filtrage sur les vols Air France et les avions moyen courrier : A320 family
    
    vols_MC = vols[vols['Type exploitation']=='Air France']
    vols_MC = vols_MC[vols_MC['Type avion réalisé'].apply(lambda x: (x=='318' or x=='319' or x=='320' or x=='321'))]
    
    #Mise en forme des dates
        
    vols_MC['Date départ prévue TU'] = vols_MC['Date départ prévue TU'].apply(lambda x: x[:10])
    vols_MC['Date départ réalisée TU'] = vols_MC['Date départ réalisée TU'].apply(lambda x: x[:10])
    vols_MC['Date arrivée prévue TU'] = vols_MC['Date arrivée prévue TU'].apply(lambda x: x[:10])
    vols_MC['Date arrivée réalisée TU'] = vols_MC['Date arrivée réalisée TU'].apply(lambda x: x[:10])
    
    
    #Création de la date départ prévue DDP
    dateetheure=vols_MC['Date départ prévue TU']+vols_MC['Heure départ prévue TU']
    vols_MC = vols_MC.assign(DDP=pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M'))
    
    #Création de la date départ réalisée DDR
    dateetheure=vols_MC['Date départ réalisée TU']+vols_MC['Heure départ réalisée TU']
    vols_MC = vols_MC.assign(DDR=pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M'))
    
    #Création de la date arrivée prévue DAP
    dateetheure=vols_MC['Date arrivée prévue TU']+vols_MC['Heure arrivée prévue TU']
    vols_MC = vols_MC.assign(DAP=pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M'))
    
    #Création de la date départ prévue DAR
    dateetheure=vols_MC['Date arrivée réalisée TU']+vols_MC['Heure arrivée réalisée TU']
    vols_MC = vols_MC.assign(DAR=pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M'))
    
    
    #Calcul de retard au départ en minutes : Retard_D
    Duree = vols_MC.DDR - vols_MC.DDP
    vols_MC = vols_MC.assign(Retard_D = Duree.apply(lambda x: x.total_seconds()/60))
    
    #Calcul de retard à l'arrivée en minutes : Retard_A
    Duree = vols_MC.DAR - vols_MC.DAP
    vols_MC = vols_MC.assign(Retard_A = Duree.apply(lambda x: x.total_seconds()/60))
    
    #jour de la semaine
    week_day = vols_MC.DDR.dt.day_name()
    day = vols_MC.DDR.dt.dayofweek
    #Creation de la colonne Week day
    vols_MC = vols_MC.assign(Week_day= week_day)
    vols_MC = vols_MC.assign(day_index= day)
    
    vols_MC.to_csv('./Data/vols_MC_cleaned.csv')

    return vols_MC

def simplify_retards(df):
    df.Retard_D = df.Retard_D.fillna(1000000)
    bins = (-1000, -10, 10, 30, 60, 300, 100001,1000001)
    group_names = ['En avance', "A l'heure", 'Moins de 30 min', 'Entre 30min et 1H', 'Entre 1H et 3H', 'Plus de 3H', "Pas d'info"]
    categories = pandas.cut(df.Retard_D, bins, labels=group_names)
    df = df.assign(Cat_retard = categories)
    return df

vols_MC = data_cleaning(vols)
vols_MC = simplify_retards(vols_MC)
vols_MC.to_csv('./Data/vols_MC_cleaned.csv')


