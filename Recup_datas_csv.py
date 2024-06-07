# -*- coding: utf-8 -*-
"""
Created on 03/11/2021

@author: B.Lefebvre
"""

# %% Imports the necessary libraries
from csv import reader
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import numpy as np
import math

# %% Variables globales
# us = 1e-6                                         # conversion éventuelle en µs
path_data = 'C:/Users/b.lefebvre/Documents/Work/Python/RecupDataOscillo/Donnees/'
# file= path_data + 'tek0000ALL2.csv'
file = path_data + 'Tek004_ALL.csv'

# %%
# -------------------------EXTRACT DATA FROM CSV--------------------------
# open file in read mode
with open(file, 'r') as read_obj:
    line_count = 1
    en_tete = []
    time = []
    ch1 = []
    ch2 = []
    ch3 = []
    ch4 = []  # -/!\- à rajouter/diminuer, en fonction du nombre de courbes
    ch1_interpol = []
    ch2_interpol = []
    ch3_interpol = []
    ch4_interpol = []  # -/!\- à rajouter/diminuer, en fonction du nombre de courbes

    csv_reader = reader(read_obj, delimiter=',')  # pass the file object to reader() to get the reader object

    # --------------Calcul du nombre de ligne d'en-tête----------------
    line = read_obj.readline()
    # print(header)
    while not line.startswith('TIME'):
        # en_tete.append(line)
        line = read_obj.readline()
        line_count += 1
        print(line)
    nbre_lignes_entete = line_count
    print('Nombre de ligne d\'en-tête :', nbre_lignes_entete)
    # print(line[1])
    # print(list(line))
    v = line.split(',')
    print(v[1])
    print(len(v))
    print(v[4])

    # --------------Elimination des lignes d'en-tête----------------
    # for i in range(nbre_lignes_entete):
    # header = next(csv_reader)    ==> on passe successivement les lignes d'en-tête
    # en_tete.append(str(header))  ==>pour afficher plus loin les lignes d'en-tête
    # x = np.array(en_tete)
    # y = x.reshape(-1,1) #transformation d'un vecteur ligne en vecteur colonne
    # print("\nLignes d''entête :")
    # print(y)

    # --------Stockage dans des listes de toutes les colonnes de l'objet "csv-reader"
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        # on élimine les valeurs non numériques
        if (not math.isinf(float(row[1])) or not math.isnan(float(row[1]))
                or not math.isinf(float(row[2])) or not math.isnan(float(row[2]))
                or not math.isinf(float(row[3])) or not math.isnan(float(row[3]))
                or not math.isinf(float(row[4])) or not math.isnan(float(row[4]))):
            # time.append(float(row[0]) / us)
            time.append(float(row[0]))
            ch1.append(float(row[1]))
            ch2.append(float(row[2]))
            ch3.append(float(row[3]))
            ch4.append(float(row[4]))  # -/!\- à rajouter/diminuer, en fonction du nombre de courbes
            line_count += 1
    print(f'Processed {line_count} lines.')  # on affiche le nombre de lignes scrutées

    # %%
    # -------------------------INTERPOLATION DES COURBES--------------------------
    time_interpol = np.linspace(min(time), max(time), 100000)  # interpolation linéaire sur 10000 points
    ch1_interpol = np.interp(time_interpol, time, ch1)
    ch2_interpol = np.interp(time_interpol, time, ch2)
    ch3_interpol = np.interp(time_interpol, time, ch3)
    ch4_interpol = np.interp(time_interpol, time, ch4)  # -/!\- à rajouter/diminuer, en fonction du nombre de courbes

    # %%
    # -------------------------FILTRAGE DE CERTAINES COURBES--------------------------
    # ch2_filtree = savgol_filter(ch2, 1000, 3)
    ch2_filtree = savgol_filter(ch2, 1000, 2)
    ch2_filtree = list[float](ch2_filtree)

# %%
# -------------------------PLOT ON SCREEN UNE SEULE COURBE voie CH1 --------------------------
# plt.subplots() is a function that returns a tuple containing a figure and axes object(s), 
# Thus when using : fig, ax = plt.subplots() you unpack this tuple into the variables fig and ax,
# Having "fig" is useful if you want to change figure-level attributes or save the figure as an
# image file later (e.g. with fig.savefig('yourfilename.png'))

# On bloque le mode interactif (plt.ion()), de manière à ce que toutes les figures puissent être affichées en même temps
# En effet, la commande : plt.show() affiche la courbe, mais bloque le code jusqu'à ce qu'on ferme la fenêtre
# Voir la boucle "for" à la fin de la séquence
plt.ioff()

fig1, ax1 = plt.subplots()
fig1.suptitle('\nForme d\'onde de la commande du contacteur NC TELAAC', fontsize=16, fontstyle='normal', weight='bold')
line1, = ax1.plot([1], label="Tension aux bornes de l'alim de puissance", color='y', linewidth=2, linestyle='-')
ax1.plot(time, ch1, '-y', linewidth=2)
# ax1.set_title('Tension', fontfamily='arial', loc='left', fontsize='medium', weight='bold', color='y')
ax1.set_xlabel('Temps (s)')
ax1.set_ylabel('Tension (V)')
ax1.grid()
ax1.legend(handles=[line1], loc='upper right')
ax1.set_ylim(-2, 2)

# %%
# -------------------------PLOT ON SCREEN PLUSIEURS COURBES--------------------------

# 1-------Plot des valeurs interpolées-------------

# affichage pleine page(constrained_layout), on partage l'axe des x(sharex) et axes Y indépendants(sharey)
# -/!\- à rajouter/diminuer, en fonction du nombre de courbes
# fig2, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, constrained_layout=True, sharex=True, sharey=False)
# fig2, (ax3, ax4) = plt.subplots(2, 1, constrained_layout=True, sharex=True, sharey=False)
# fig2.suptitle('\nMaquette CEM - Commande phase-shift 130° - Vbus = 1100VDC', fontsize=16, fontstyle='normal',
# weight='bold') ax1.plot(time_interpol, ch1_interpol, '-y',linewidth=1, label='V') #le "label" ne fonctionne pas (
# pas compris pourquoi) ax1.set_title('Tension de mode commun RSIL', fontfamily='arial', loc='left',
# fontsize='medium', weight='bold', color='y') #FFD700 ax1.set_ylabel('(V)') ax1.grid() ax1.legend(handles=[line1],
# loc ='center right')

fig2, ax2 = plt.subplots()
fig2.suptitle('\nForme d\'onde de la commande du contacteur NC TELAAC', fontsize=16, fontstyle='normal', weight='bold')
line2, = ax2.plot([2], label="Courant consommé par l'alim de puissance", color='b', linewidth=2, linestyle='-')
# ax2.plot(time_interpol, ch2_interpol, '-b', linewidth=1)
ax2.plot(time, ch2, '-b', linewidth=1)


# %%
# -------------------------DETECTION DES EXTREMA D'UNE COURBE DE POINTS--------------------------
def annot_max(x, y, reperex, reperey, col, ax=None):
    # xmax = x[np.argmax(x)]
    # ymax = y.max()
    ymax = max(y)
    xpos = y.index(ymax)
    xmax = x[xpos]
    text = "x={:.3f}, y={:.3f}".format(xmax, ymax)
    if not ax:
        ax = plt.gca()
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60", color=col)
        kw = dict(xycoords='data', textcoords="axes fraction",
                  arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top", color=col)
        ax.annotate(text, xy=(xmax, ymax), xytext=(reperex, reperey), **kw)


annot_max(time, ch2, 0.6, 0.96, 'blue')
ax2.set_ylim(-10, 20)

ax2.plot(time, ch2_filtree, 'r', linewidth=1)
ax2.set_ylabel('courant (A)')
ax2.grid()
ax2.legend(handles=[line2], loc='center right')
annot_max(time, ch2_filtree, 0.6, 0.56, 'red')

fig3, (ax3, ax4) = plt.subplots(2, 1, constrained_layout=True, sharex=True, sharey=False)
fig3.suptitle('\nSignal de commande', fontsize=16, fontstyle='normal', weight='bold')
line3, = ax3.plot([3], label="Courant de commande", color='b', linewidth=2, linestyle='-')
line4, = ax4.plot([4], label="Etat du contact de puissance", color='r', linewidth=2, linestyle='-')
ax3.plot(time, ch3, '-b', linewidth=1)
ax4.plot(time, ch4, '-r', linewidth=1)
ax4.set_xlabel('Temps (s)')
ax3.set_ylabel('Courant (A)')
ax4.set_ylabel('Tension (V)')
ax3.grid()
ax4.grid()
ax3.legend(handles=[line1], loc='upper right')
ax4.legend(handles=[line1], loc='upper right')

# line3, = ax.plot([3],
# label ="Tension Drain-Source Vds - Q2(low side)",
#                 color='r',
#                 linewidth=2,
#                 linestyle='-')
# ax3.plot(time_interpol, ch3_interpol, '-r', linewidth=1)
# ax3.set_title('Tension Drain-Source Vds - Q2(low side)', fontfamily='arial', loc='left', fontsize='medium',
# weight='bold', color='r')
# ax3.set_xlabel('Time (2ms/div)')
# ax3.set_ylabel('Overvoltage Long Pulse - Zone B (V)')
# ax3.grid()
# ax3.legend(handles=[line3], loc ='center right')

# line4, = ax.plot([4],
# label ="Tension Drain-Source Vds - Q4(low side)",
#                 color='g',
#                 linewidth=2,
#                 linestyle='-')
# ax4.plot(time_interpol, ch4_interpol, '-g', linewidth=1)
# ax4.set_title('Tension Drain-Source Vds - Q4(low side)', fontfamily='arial', loc='left', fontsize='medium',
# weight='bold', color='g')
# ax4.set_xlabel('Time (2ms/div)')
# ax4.set_ylabel('I_line (A)')
# ax4.grid()
# ax4.legend(handles=[line4], loc ='center right')


# 2-------Plot des valeurs brutes-------------

# affichage pleine page(constrained_layout), on partage l'axe des x(sharex) et axes Y indépendants(sharey)
# -/!\- à rajouter/diminuer, en fonction du nombre de courbes
# fig3, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, constrained_layout=True, sharex=True, sharey=False)
# fig3, (ax3, ax4) = plt.subplots(2, 1, constrained_layout=True, sharex=True, sharey=False)
# fig3.suptitle('\nMaquette CEM - Commande phase-shift 130° - Vbus = 1100VDC',
# fontsize=16, fontstyle='normal', weight='bold')

# ax1.plot(time, ch1, '-y',linewidth=0.5, label='Tension de mode commun RSIL')
# ax1.set_title('Tension de mode commun RSIL', fontfamily='arial', loc='left', fontsize='medium',
# weight='bold', color='y') #FFD700
# ax1.set_ylabel('(V)')
# ax1.grid()
# ax1.legend(handles=[line1], loc ='center right')

# ax2.plot(time, ch2, '-b', linewidth=0.5)
# ax2.set_title('Courant dans la charge', fontfamily='arial', loc='left', fontsize='medium', weight='bold', color='b')
# ax2.set_ylabel('(A)')
# ax2.grid()
# ax2.legend(handles=[line2], loc ='center right')

# ax3.plot(time, ch3, '-r', linewidth=0.5)
# ax3.set_title('Tension Drain-Source Vds - Q2(low side)', fontfamily='arial', loc='left', fontsize='medium',
# weight='bold', color='r')
# ax3.set_ylabel('(V)')
# ax3.grid()
# ax3.legend(handles=[line3], loc ='center right')

# ax4.plot(time, ch4, '-g', linewidth=0.5)
# ax4.set_title('Tension Drain-Source Vds - Q4(low side)', fontfamily='arial', loc='left', fontsize='medium',
# weight='bold', color='g')
# ax4.set_xlabel('Temps (µs)')
# ax4.set_ylabel('(V)')
# ax4.grid()
# ax4.legend(handles=[line4], loc='center right')

# %%
# -------------------------AFFICHAGE DES COURBES--------------------------
# Affichage des courbes à la suite, grâce à la commande "plt.ioff()" du début
plt.show()
plt.close()


# %%
# -------------------------ENREGISTREMENT FICHIERS--------------------------

# fig3.savefig('figures\\Plot_valeurs_brutes.png')
# fig1.savefig('figures\\Plot_single.pdf')
# Attention : il faut fermer manuellement les figures pour que les commandes soient prises en compte
def save_fig(f1, f2, f3):
    fig1.savefig(f1, dpi=600, format='pdf')
    fig2.savefig(f2, dpi=600, format='pdf')
    fig3.savefig(f3, dpi=600, format='pdf')
    print('Files saved !!')


save_fig('Figures\\Plot1.pdf', 'Figures\\Plot2.pdf', 'Figures\\Plot3.pdf')
