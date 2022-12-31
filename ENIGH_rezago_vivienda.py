#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 17:52:57 2022

@author: ja
"""

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

# Tareas

    # Microdatos INEGI cuadro Viviendas tercer trimestre 2022
ENIGH_2022 = pd.read_csv('/home/ja/Descargas/enigh2020_ns_viviendas_csv/viviendas.csv', encoding='unicode_escape',low_memory = False)


    # Estimar el número de viviendas con rezago habiacional a niver nacional y por entidad federativa de acuerdo con la metodología de la Conavi
vivienda = ["ï»¿folioviv","factor"]
        # Identificación de las viviendas por sus materiales en paredes, en techo y pisos.
        
materiales = ["mat_pared",
              "mat_techos",
              "mat_pisos"]
        
        # Residentes por cuarto en cada vivienda
residentes = ["tot_resid",
              "num_cuarto"]

        # Excusado
excusado = ["excusado"]

selección = vivienda + materiales +  residentes + excusado

ENIGH_2022 = ENIGH_2022[selección]

del excusado, materiales, residentes, selección, vivienda  

        # Cálculo
            # Materiales deteriorados
pared_det = list(np.where(ENIGH_2022["mat_pared"].isin([1,2,4,5,9]),1,0))

techo_det = list(np.where(ENIGH_2022["mat_techos"].isin([1,2,6,99]),1,0))

mat_det = [1 if i==1 or j==1 else 0 for i,j in zip(pared_det,techo_det)]

del pared_det, techo_det

            # Materiales regulares
pared_reg = list(np.where(ENIGH_2022["mat_pared"].isin([3,6]),1,0))

techo_reg = list(np.where(ENIGH_2022["mat_techos"].isin([3,4,7,9]),1,0))

piso_reg = list(np.where(ENIGH_2022["mat_pisos"].isin([1,9]),1,0))

mat_reg = [1 if h==1 or i==1 or j==1 else 0 for h,i,j in zip(pared_reg,techo_reg,piso_reg)]

del pared_reg, techo_reg, piso_reg

            # Precariedad del espacio de vivienda
res_cuarto = ENIGH_2022["tot_resid"]/ENIGH_2022["num_cuarto"]

hacin = [1 if i > 2.5 else 0 for i in res_cuarto]

excu = list(np.where(ENIGH_2022["excusado"].eq(1),0,1))

prec_esp = [1 if  i==1 or j==1 else 0 for i,j in zip(hacin,excu)]

del res_cuarto, hacin, excu

### Rezago ###

rezago = [1 if h==1 or i==1 or j==1 else 0 for h,i,j in zip(mat_det,mat_reg,prec_esp)]
rezago = pd.DataFrame(rezago)

# Presentación de los resultados
conavi_rez = pd.concat([ENIGH_2022[["ï»¿folioviv","factor"]],rezago], axis = 1)
conavi_rez.columns = ["folioviv","factor","rezago"]

conavi_rez["rezago"] = conavi_rez["rezago"].astype("category")
conavi_rez["rezago"] = conavi_rez["rezago"].cat.rename_categories({0:"sin rezago habitacional",
                                                                   1:"con rezago habitacional"})

conavi_rez["mat_det"] = mat_det
conavi_rez["mat_det"] = conavi_rez["mat_det"].astype("category")
conavi_rez["mat_det"] = conavi_rez["mat_det"].cat.rename_categories({0:"sin materiales deteriorados",
                                                                     1:"con materiales deteriorados"})


conavi_rez["mat_reg"] = mat_reg
conavi_rez["mat_reg"] = conavi_rez["mat_reg"].astype("category")
conavi_rez["mat_reg"] = conavi_rez["mat_reg"].cat.rename_categories({0:"sin materiales regulares",
                                                                     1:"con materiales regulares"})

conavi_rez["prec_esp"] = prec_esp
conavi_rez["prec_esp"] = conavi_rez["prec_esp"].astype("category")
conavi_rez["prec_esp"] = conavi_rez["prec_esp"].cat.rename_categories({0:"sin precariedad en los espacios",
                                                                       1:"con precariedad en los espacios"})
  
del mat_det, mat_reg, prec_esp, rezago
    # Rezago a nivel nacional
plt.style.use("fivethirtyeight")

    # Gráfica de pie de los hogares con rezago de vivienda a nivel nacional
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{:.1f}%\n({v:d})'.format(pct, v=val)
    return my_format

plt.pie(conavi_rez.groupby("rezago")["factor"].sum(), 
        labels = ["sin rezago", "con rezago"],
        shadow = True,
        colors = ('lightskyblue','lightcoral'),
        autopct = autopct_format(conavi_rez.groupby("rezago")["factor"].sum()),
        explode = (0.05,0.2))
plt.title("Viviendas con rezago habitacional. México 2022")
plt.text(-2.55,-1.5,"Fuente: Elaboración propia con base en los datos de la ENIGH 2022")
plt.savefig('/home/ja/Documentos/plot_1.png', dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()     

    # Gráfica de pie de las viviendas con material deteriorado a nivel nacional
plt.pie(conavi_rez.groupby("mat_det")["factor"].sum(), 
        labels = ["sin materiales deteriorados", "con materiales deteriorados"],
        shadow = True,
        colors = ('lightskyblue','lightcoral'),
        autopct = autopct_format(conavi_rez.groupby("mat_det")["factor"].sum()),
        explode = (0.5,0.4))
plt.title("Viviendas con materiales deteriorados. México 2022")
plt.text(-2.55,-1.5,"Fuente: Elaboración propia con base en los datos de la ENIGH 2022")
plt.savefig('/home/ja/Documentos/plot_2.png', dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()

    # Gráfca de íe de las viviendas con materiales regulares a nivel nacional
plt.pie(conavi_rez.groupby("mat_reg")["factor"].sum(), 
        labels = ["sin materiales regulares", "con materiales regulares"],
        shadow = True,
        colors = ('lightskyblue','lightcoral'),
        autopct = autopct_format(conavi_rez.groupby("mat_reg")["factor"].sum()),
        explode = (0.2,0.1))
plt.title("Viviendas con materiales regulares. México 2022")
plt.text(-2.55,-1.5,"Fuente: Elaboración propia con base en los datos de la ENIGH 2022")
plt.savefig('/home/ja/Documentos/plot_3.png',dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()

    # Gráfca de íe de las viviendas con precariedad en los espacios
plt.pie(conavi_rez.groupby("prec_esp")["factor"].sum(), 
        labels = ["sin precariedad en espacios", "con precariedad en espacios"],
        shadow = True,
        colors = ('lightskyblue','lightcoral'),
        autopct = autopct_format(conavi_rez.groupby("prec_esp")["factor"].sum()),
        explode = (0.5,0.3))
plt.title("Viviendas con precariedad en los espacios. México 2022")
plt.text(-2.55,-1.5,"Fuente: Elaboración propia con base en los datos de la ENIGH 2022")
plt.savefig('/home/ja/Documentos/plot_4.png', dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()

    # Cuadro con el número de viviendas totales, con rezago habitacional y el porcentaje de viviendas con rezago habitacional

conavi_rez["folioviv"] = conavi_rez["folioviv"].astype("str")
conavi_rez["folioviv"] = [i.zfill(10) for i in conavi_rez["folioviv"]]

conavi_rez["estados"] = [i[0:2] for i in conavi_rez.folioviv]
conavi_rez["estados"] = conavi_rez["estados"].astype("int64")

estados = [conavi_rez["estados"] == 1,
           conavi_rez["estados"] == 2,
           conavi_rez["estados"] == 3,
           conavi_rez["estados"] == 4,
           conavi_rez["estados"] == 5,
           conavi_rez["estados"] == 6,
           conavi_rez["estados"] == 7,
           conavi_rez["estados"] == 8,
           conavi_rez["estados"] == 9,
           conavi_rez["estados"] == 10,
           conavi_rez["estados"] == 11,
           conavi_rez["estados"] == 12,
           conavi_rez["estados"] == 13,
           conavi_rez["estados"] == 14,
           conavi_rez["estados"] == 15,
           conavi_rez["estados"] == 16,
           conavi_rez["estados"] == 17,
           conavi_rez["estados"] == 18,
           conavi_rez["estados"] == 19,
           conavi_rez["estados"] == 20,
           conavi_rez["estados"] == 21,
           conavi_rez["estados"] == 22,
           conavi_rez["estados"] == 23,
           conavi_rez["estados"] == 24,
           conavi_rez["estados"] == 25,
           conavi_rez["estados"] == 26,
           conavi_rez["estados"] == 27,
           conavi_rez["estados"] == 28,
           conavi_rez["estados"] == 29,
           conavi_rez["estados"] == 30,
           conavi_rez["estados"] == 31,
           conavi_rez["estados"] == 32]

conavi_rez["estados"] = np.select(estados,["Aguascalientes",
                                 "Baja California",
                                 "Baja California Sur",
                                 "Campeche",
                                 "Coahuila de Zaragoza",
                                 "Colima",
                                 "Chiapas",
                                 "Chihuahua",
                                 "Ciudad de México",
                                 "Durango",
                                 "Guanajuato",
                                 "Guerrero",
                                 "Hidalgo",
                                 "Jalisco",
                                 "México",
                                 "Michoacán de Ocampo",
                                 "Morelos",
                                 "Nayarit",
                                 "Nuevo León",
                                 "Oaxaca",
                                 "Puebla",
                                 "Querétaro",
                                 "Quintana Roo",
                                 "San Luis Potosí",
                                 "Sinaloa",
                                 "Sonora",
                                 "Tabasco",
                                 "Tamaulipas",
                                 "Tlaxcala",
                                 "Veracruz de Ignacio de la Llave",
                                 "Yucatán",
                                 "Zacatecas"])

del estados

    # Tabla rezagos
estados_conavi_rez = pd.DataFrame(conavi_rez.groupby(["estados","rezago"])["factor"].sum())
estados_conavi_rez.columns = ["Viviendas"]
estados_conavi_rez = estados_conavi_rez.reset_index()

estados_conavi_con_rez = estados_conavi_rez[estados_conavi_rez["rezago"] == "con rezago habitacional"]
estados_conavi_con_rez = estados_conavi_con_rez[["estados","Viviendas"]]
estados_conavi_con_rez = estados_conavi_con_rez.set_index("estados")

estados_conavi_sin_rez = estados_conavi_rez[estados_conavi_rez["rezago"] == "sin rezago habitacional"]
estados_conavi_sin_rez = estados_conavi_sin_rez[["estados","Viviendas"]]
estados_conavi_sin_rez = estados_conavi_sin_rez.set_index("estados")

estados_conavi_rez = pd.concat([estados_conavi_con_rez,estados_conavi_sin_rez], axis = 1)
estados_conavi_rez.columns = ["Con rezago","Sin rezago"]
estados_conavi_rez.insert(0, "Viviendas", estados_conavi_rez["Con rezago"] + estados_conavi_rez["Sin rezago"])
estados_conavi_rez["% con rezago"] = (estados_conavi_rez["Con rezago"]/estados_conavi_rez["Viviendas"])*100
estados_conavi_rez = estados_conavi_rez.sort_index()

del estados_conavi_con_rez, estados_conavi_sin_rez
    
    # Tabla materiales deteriorados
estados_conavi_mat_det = pd.DataFrame(conavi_rez.groupby(["estados","mat_det"])["factor"].sum())
estados_conavi_mat_det.columns = ["Viviendas"]
estados_conavi_mat_det = estados_conavi_mat_det.reset_index()

estados_conavi_con_mat_det = estados_conavi_mat_det[estados_conavi_mat_det["mat_det"] == "con materiales deteriorados"]
estados_conavi_con_mat_det = estados_conavi_con_mat_det[["estados","Viviendas"]]
estados_conavi_con_mat_det = estados_conavi_con_mat_det.set_index("estados")

estados_conavi_sin_mat_det = estados_conavi_mat_det[estados_conavi_mat_det["mat_det"] == "sin materiales deteriorados"]
estados_conavi_sin_mat_det = estados_conavi_sin_mat_det[["estados","Viviendas"]]
estados_conavi_sin_mat_det = estados_conavi_sin_mat_det.set_index("estados")

estados_conavi_mat_det = pd.concat([estados_conavi_con_mat_det,estados_conavi_sin_mat_det], axis = 1)
estados_conavi_mat_det.columns = ["Con deterioro","Sin deterioro"]
estados_conavi_mat_det.insert(0, "Viviendas", estados_conavi_mat_det["Con deterioro"] + estados_conavi_mat_det["Sin deterioro"])
estados_conavi_mat_det["% con deterioro"] = (estados_conavi_mat_det["Con deterioro"]/estados_conavi_mat_det["Viviendas"])*100
estados_conavi_mat_det = estados_conavi_mat_det.sort_index()

del estados_conavi_con_mat_det, estados_conavi_sin_mat_det

    # Tabla de materiales regulares
estados_conavi_mat_reg = pd.DataFrame(conavi_rez.groupby(["estados","mat_reg"])["factor"].sum())
estados_conavi_mat_reg.columns = ["Viviendas"]
estados_conavi_mat_reg = estados_conavi_mat_reg.reset_index()

estados_conavi_con_mat_reg = estados_conavi_mat_reg[estados_conavi_mat_reg["mat_reg"] == "con materiales regulares"]
estados_conavi_con_mat_reg = estados_conavi_con_mat_reg[["estados","Viviendas"]]
estados_conavi_con_mat_reg = estados_conavi_con_mat_reg.set_index("estados")

estados_conavi_sin_mat_reg = estados_conavi_mat_reg[estados_conavi_mat_reg["mat_reg"] == "sin materiales regulares"]
estados_conavi_sin_mat_reg = estados_conavi_sin_mat_reg[["estados","Viviendas"]]
estados_conavi_sin_mat_reg = estados_conavi_sin_mat_reg.set_index("estados")

estados_conavi_mat_reg = pd.concat([estados_conavi_con_mat_reg,estados_conavi_sin_mat_reg], axis = 1)
estados_conavi_mat_reg.columns = ["Con material regular","Sin material regular"]
estados_conavi_mat_reg.insert(0, "Viviendas", estados_conavi_mat_reg["Con material regular"] + estados_conavi_mat_reg["Sin material regular"])
estados_conavi_mat_reg["% con material regular"] = (estados_conavi_mat_reg["Con material regular"]/estados_conavi_mat_reg["Viviendas"])*100
estados_conavi_mat_reg = estados_conavi_mat_reg.sort_index()

del estados_conavi_con_mat_reg, estados_conavi_sin_mat_reg

    # Tabla de precariedad en los espacios
estados_conavi_prec_esp = pd.DataFrame(conavi_rez.groupby(["estados","prec_esp"])["factor"].sum())
estados_conavi_prec_esp.columns = ["Viviendas"]
estados_conavi_prec_esp = estados_conavi_prec_esp.reset_index()

estados_conavi_con_prec_esp = estados_conavi_prec_esp[estados_conavi_prec_esp["prec_esp"] == "con precariedad en los espacios"]
estados_conavi_con_prec_esp = estados_conavi_con_prec_esp[["estados","Viviendas"]]
estados_conavi_con_prec_esp = estados_conavi_con_prec_esp.set_index("estados")

estados_conavi_sin_prec_esp = estados_conavi_prec_esp[estados_conavi_prec_esp["prec_esp"] == "sin precariedad en los espacios"]
estados_conavi_sin_prec_esp = estados_conavi_sin_prec_esp[["estados","Viviendas"]]
estados_conavi_sin_prec_esp = estados_conavi_sin_prec_esp.set_index("estados")

estados_conavi_prec_esp = pd.concat([estados_conavi_con_prec_esp,estados_conavi_sin_prec_esp], axis = 1)
estados_conavi_prec_esp.columns = ["Con precariedad","Sin precariedad"]
estados_conavi_prec_esp.insert(0, "Viviendas", estados_conavi_prec_esp["Con precariedad"] + estados_conavi_prec_esp["Sin precariedad"])
estados_conavi_prec_esp["% con precariedad"] = (estados_conavi_prec_esp["Con precariedad"]/estados_conavi_prec_esp["Viviendas"])*100
estados_conavi_prec_esp = estados_conavi_prec_esp.sort_index()

del estados_conavi_con_prec_esp, estados_conavi_sin_prec_esp


    # Poĺigonos para el mapa
entidades = gpd.read_file("/media/ja/Andres data/Descargas/Entidades y Municipios/00ent.shp")

    # Mapa rezagos
mex_rezagos = entidades.merge(estados_conavi_rez, left_on = 'NOMGEO', right_index = True, how = 'left')
mex_rezagos.plot(column = "% con rezago",
                 legend = True,
                 cmap = 'Blues',
                 legend_kwds = {'orientation': "horizontal",
                                'label':"% con rezago"})
plt.title("Viviendas con rezago habitacional. México 2022")
plt.axis('off')    
plt.savefig('/home/ja/Documentos/map_1.png', dpi = 300, bbox_inches='tight')
plt.show()

    # Mapa de viviendas con materiales deteriorados
mex_rezagos = entidades.merge(estados_conavi_mat_det, left_on = 'NOMGEO', right_index = True, how = 'left')
mex_rezagos.plot(column = "% con deterioro",
                 legend = True,
                 cmap = 'Greens',
                 legend_kwds = {'orientation': "horizontal",
                                'label':"% con deterioro"})
plt.title("Viviendas con materiales deteriorados. México 2022")
plt.axis('off')    
plt.savefig('/home/ja/Documentos/map_2.png', dpi = 300, bbox_inches='tight')
plt.show()

    # Mapa de viviendas con materiales regulares
mex_rezagos = entidades.merge(estados_conavi_mat_reg, left_on = 'NOMGEO', right_index = True, how = 'left')
mex_rezagos.plot(column = "% con material regular",
                 legend = True,
                 cmap = 'Oranges',
                 legend_kwds = {'orientation': "horizontal",
                                'label':"% con deterioro"})
plt.title("Viviendas con materiales dregulares. México 2022")
plt.axis('off')    
plt.savefig('/home/ja/Documentos/map_3.png', dpi = 300, bbox_inches='tight')
plt.show()
    
    # Mapa de viviendas con precariedad en los espacios
mex_rezagos = entidades.merge(estados_conavi_prec_esp, left_on = 'NOMGEO', right_index = True, how = 'left')
mex_rezagos.plot(column = "% con precariedad",
                 legend = True,
                 cmap = 'Greys',
                 legend_kwds = {'orientation': "horizontal",
                                'label':"% con deterioro"})
plt.title("Viviendas con precariedad en los espacios. México 2022")
plt.axis('off')    
plt.savefig('/home/ja/Documentos/map_4.png', dpi = 300, bbox_inches='tight')
plt.show()