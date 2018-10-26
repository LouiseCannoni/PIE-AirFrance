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
    
    vols_MC.to_csv('./Data/vols_MC_cleaned.csv')

    return vols_MC

vols_MC = data_cleaning(vols)


def chainage(vols_MC):
    
    #Trouver les chainages en identifiant l'heure d'arrivée de dernier vol de chaque chainage
    HA_chainage = vols_MC.groupby(['Date départ réalisée TU','Immatriculation'])[['Heure arrivée réalisée TU']].max().unstack('Immatriculation')
    HA_chainage_mat = HA_chainage.values
    HA_chainage.head()
    
    #Liste des immatriculations
    listColNames=np.asarray(list(HA_chainage.columns)).T
    listColNames=listColNames[1]
    
    #Liste des dates de départ
    listLigNames=np.asarray(list(HA_chainage.index))
    
    #Classer dans une matrice le numéro de ligne dans la BDD de dernier vol de chaque chainage
    
    Dernier_vol_chainage = np.array([[0 for i in range(len(listColNames))] for j in range(len(listLigNames))])
    for i in range(len(listColNames)):
        vols_imm = vols_MC[vols_MC['Immatriculation']==listColNames[i]]
        for j in range(len(listLigNames)):
            if type(HA_chainage_mat[j,i]) == float:
                if isnan(float(HA_chainage_mat[j,i])):
                    #Pas d'information sur l'heure d'arrivée de l'avion : on choisit une valeur négative afin de pouvoir l'éliminer
                    Dernier_vol_chainage[j,i] = -1 
                    
            else:
    
                vols_date = vols_imm[vols_imm['Date arrivée réalisée TU']==listLigNames[j]]
                vols_heure = vols_date[vols_date['Heure arrivée réalisée TU']==HA_chainage_mat[j,i]]
                if len(vols_heure) == 0:
                    #L'avion n'a pas voler le jour j : on choisit une valeur négative afin de pouvoir l'éliminer
                    Dernier_vol_chainage[j,i] = -2
                else:
                    Dernier_vol_chainage[j,i] = vols_heure.index[0]
    
    
    #Construire une Dataframe contenant tous les chainages valides avec les informations correspondantes
    
    Variables =['N° Ligne dernier vol de chainage','Identifiant dernier vol','Immatriculation','Date arrivée réalisée TU'
                ,'Retard_A dernier vol','Type avion réalisé']
    
    Chainage_valide=[]
    for i in range(len(listLigNames)):
        for j in range(len(listColNames)):
            if Dernier_vol_chainage[i,j]>= 0:
                Chainage_valide.append(Dernier_vol_chainage[i,j])
    
    List1=[]
    List2=[]
    List3=[]
    List4=[]
    List5=[]
    for i in range(len(Chainage_valide)):
        List1.append(vols.iloc[Chainage_valide[i],:]['Identifiant vol'])
        List2.append(vols.iloc[Chainage_valide[i],:]['Immatriculation'])
        List3.append(vols.iloc[Chainage_valide[i],:]['Date arrivée réalisée TU'])
        List4.append(vols.iloc[Chainage_valide[i],:]['Retard_A'])
        List5.append(vols.iloc[Chainage_valide[i],:]['Type avion réalisé'])
    
    Chainage_var = pandas.DataFrame({Variables[0]: Chainage_valide, Variables[1]: List1, 
                                     Variables[2]: List2, Variables[3]: List3, Variables[4]: List4, Variables[5]: List5})
    
    Chainage_var.to_csv('./Data/chainages.csv')

    return Chainage_var
    
chainage(vols_MC)
