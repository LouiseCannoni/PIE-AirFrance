#Valeurs aberrantes
import pandas
import numpy as np
import matplotlib.pyplot as plt

vols_MC = pandas.read_csv("./Data/vols_MC_cleaned.csv",sep=',',decimal=b',')


def retrait_valeurs_aberrantes(vols_MC):
    #moyenne des retards à l'arrivée 
    moy_retard = np.mean(vols_MC['Retard_D'])
    #ecart type à l'arrivée
    ecarttype_retard = np.std(vols_MC['Retard_D'])

    #vols sans valeurs aberrantes
    vols_MC_opt = vols_MC[vols_MC['Retard_D'].apply(lambda x: (x < moy_retard + 20*ecarttype_retard))]
    
    return vols_MC_opt


#boxplot du retard / type d'avion (retard non moyen) avec valeurs aberrantes
vols_MC.boxplot('Retard_D', by='Type avion réalisé', figsize=(12, 8))
plt.show()

#boxplot du retard / type d'avion (retard non moyen) SANS valeurs aberrantes
vols_opt = retrait_valeurs_aberrantes(vols_MC)
vols_opt.boxplot('Retard_D', by='Type avion réalisé', figsize=(12, 8))
plt.show()



