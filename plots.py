import pandas
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

vols = pandas.read_csv("./Data/Extract_1cut.csv",sep=',',decimal=b',')
sChainage_var = pandas.read_csv("./Data/chainages.csv",sep=',',decimal=b',')


def retard_moy_par_jour(vols_MC):
    fig = plt.figure()
    plt.subplots(figsize=(20, 5))
    plt.plot(vols_MC.groupby(['Date départ réalisée TU','Type avion réalisé'])[['Retard_D']].mean().unstack('Type avion réalisé'),linewidth=0.8, marker="+")
    plt.xticks(rotation = 'vertical')
    plt.grid(True)
    plt.legend(('A318','A319','A320','A321'))
    plt.show()
    
def retard_moy_par_aeroport(vols_MC):
    #Les aéroports ayant les plus de retard moyen
    Escale_D = vols_MC.groupby('Escale départ réalisée')[['Retard_D']]
    Escale_D_moy = Escale_D.mean()
    Escale_D_max  = Escale_D_moy[Escale_D_moy['Retard_D']>10].sort_values(by=['Retard_D'],ascending=False)

    fig = plt.figure()
    plt.subplots(figsize=(20, 7))
    plt.plot(Escale_D_max,"*")
    plt.xticks(rotation = 'vertical')
    plt.grid(True)
    plt.ylim(bottom=0)
    plt.show()
    
def aeroports_absorbeur_retard(vols_MC):
    #Les aéroports absorbeurs de retard
    Escale_D_min  = Escale_D_moy[Escale_D_moy['Retard_D']<0].sort_values(by=['Retard_D'])

    fig = plt.figure()
    plt.subplots(figsize=(20, 5))
    plt.plot(Escale_D_min,"*")
    plt.xticks(rotation = 'vertical')
    plt.grid(True)
    plt.ylim(top=0)
    plt.show()

def retard_moy_vols_type_avion(vols_MC):
    # Courbe retard moyen par chainage par jour par type d'avion

    fig = plt.figure()

    plt.subplots(figsize=(20, 5))
    plt.plot(vols_MC.groupby(['Date départ réalisée TU','Type avion réalisé'])[['Retard_D']].mean().unstack('Type avion réalisé'),linewidth=0.8, marker="+")
    plt.xticks(rotation = 'vertical')
    plt.grid(True)
    plt.legend(('A318','A319','A320','A321'))
    plt.show()
    
def retard_jour_moy_semaine(vols,vols_MC):
    #week days

    #jour de départ prévu
    dateetheure=vols_MC['Date départ prévue TU']+vols['Heure départ prévue TU']

    #conversion en format date time
    dateetheure_datetime = pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M')

    #jour de la semaine
    week_day = dateetheure_datetime.dt.day_name()
    day = dateetheure_datetime.dt.dayofweek
    #Creation de la colonne Week day
    vols_MC = vols_MC.assign(Week_day= week_day)
    vols_MC = vols_MC.assign(day_index= day)

    fig = plt.figure()
    plt.subplots(figsize=(20, 5))
    #plt.plot(Escale_D_max,"*")
    plt.plot(vols_MC.groupby(['Week_day'])[['Retard_D']].mean(),linewidth=0.8, marker="+")
    plt.xticks(rotation = 'vertical')
    plt.grid(True)
    plt.ylim(bottom=0)
    plt.title("Retard moyen par jour de la semaine")
    plt.show()

def retard_moy_type_avion(vols_MC):
    # Courbe retard moyen par avion
    fig = plt.figure()

    plt.subplots(figsize=(20, 5))
    plt.plot(vols_MC.groupby(['Type avion réalisé'])[['Retard_D']].mean(),linewidth=0.8, marker="+")
    plt.xticks(rotation = 'vertical')
    plt.grid(True)
    plt.title("Retard moyen par avion")
    plt.show()

def boxplot_retard_type_avion(vols_MC):
    vols_MC.boxplot('Retard_D', by='Type avion réalisé', figsize=(12, 8))
    plt.show()

def retard_moy_jour_semaine_type_avion(vols,vols_MC):
    fig = plt.figure()
    #jour de départ prévu
    dateetheure=vols_MC['Date départ prévue TU']+vols['Heure départ prévue TU']

    #conversion en format date time
    dateetheure_datetime = pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M')

    #jour de la semaine
    week_day = dateetheure_datetime.dt.day_name()
    day = dateetheure_datetime.dt.dayofweek
    #Creation de la colonne Week day
    vols_MC = vols_MC.assign(Week_day= week_day)
    vols_MC = vols_MC.assign(day_index= day)
    
    plt.subplots(figsize=(20, 5))
    plt.plot(vols_MC.groupby(['Week_day','Type avion réalisé'])[['Retard_D']].mean().unstack('Type avion réalisé'),linewidth=0.8, marker="+")
    plt.xticks(rotation = 'vertical')
    plt.grid(True)
    plt.legend(('A318','A319','A320','A321'))
    plt.show()
    
#Pour les chainages :
    
def retard_moy_par_jour_chainage_vols(vols_MC,Chainage_var):
    # Courbe retard moyen par jour
    fig = plt.figure()

    plt.subplots(figsize=(20, 5))
    plt.plot(vols_MC.groupby(['Date départ réalisée TU'])[['Retard_D']].mean(),linewidth=0.8, marker="+",label="Retard moyen pour les vol")
    plt.plot(Chainage_var.groupby(['Date arrivée réalisée TU'])[['Retard_A dernier vol']].mean(),linewidth=0.8, marker="+",label="Retard moyen pour les chainages")
    plt.xticks(rotation = 'vertical')
    plt.grid(True)
    plt.legend()
    plt.title("Retard moyen par jour par chaiange")
    plt.show()
    

def retard_moy_jour_semaine_chainage(vols,vols_MC,Chainage_var):
    #jour de départ prévu
    dateetheure=vols_MC['Date départ prévue TU']+vols['Heure départ prévue TU']

    #conversion en format date time
    dateetheure_datetime = pandas.to_datetime(dateetheure,format='%Y/%m/%d%H:%M')

    #jour de la semaine
    week_day = dateetheure_datetime.dt.day_name()
    day = dateetheure_datetime.dt.dayofweek
    #Creation de la colonne Week day
    Chainage_var = Chainage_var.assign(Week_day= week_day)
    Chainage_var = Chainage_var.assign(day_index= day)


    Chainage_var.head()

    fig = plt.figure()
    plt.subplots(figsize=(20, 5))
    #plt.plot(Escale_D_max,"*")
    plt.plot(Chainage_var.groupby(['Week_day'])[['Retard_A dernier vol']].mean(),linewidth=0.8, marker="+")
    plt.xticks(rotation = 'vertical')
    plt.grid(True)
    plt.ylim(bottom=0)
    plt.title("Retard moyen par jour de la semaine sur les chainages")
    plt.show()
    
def boxplot_retard_jour_semaine(Chainage_var):
    Chainage_var.boxplot('Retard_A dernier vol', by='Week_day', figsize=(12, 8))
    plt.show()

