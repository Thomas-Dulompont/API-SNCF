# https://github.com/zakariachowdhury/streamlit-map-dashboard/blob/main/streamlit_app.py
# call to render Folium map in Streamlit

import folium
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import json
import pandas as pd
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

import plotly.express as px
import plotly.graph_objects as go

from PIL import Image
from millify import millify
##########################################
##########################################


st.set_page_config(page_icon=":bar_chart:",
                layout="wide")



#########################################
#########################################
objects_par_regions = pd.read_csv('CSV/objects_par_region.csv')
geo = json.load(open("GEOJSON/regions.geojson")) # lire les données

#########################################
#########################################
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

mygrid0 = make_grid(1,6)
image = Image.open("Simplon.png")
new_image = image.resize((100, 100))
mygrid0[0][0].image(new_image)
mygrid0[0][5].image("sncf.png")


mygrid1 = make_grid(1,3)

mygrid1[0][1].markdown('## Projet : Lost in translation')
# mygrid1[0][1].markdown("###### Requêtes d'API, stockage en SQL, Folium, Plotly, Streamlit et Statistiques")
with mygrid1[0][1]:
    with st.expander("Contexte du projet"):
        st.markdown(r"""
        Data Scientist à la SNCF, votre manager vous demande de vous pencher sur un sujet particulier, la gestion des objets perdus.

En effet, chaque jour des dizaines d'objets sont perdus partout en France par les voyageurs, leur gestion est critique au niveau de la satisfaction client. Cependant le cout de leur gestion est critique également. On aimerait donc dimensionner au mieux le service en charge de les gérer mais pour cela il faut pouvoir anticiper de manière précise le volume d'objets perdus chaque jour. Votre manager a une intuition qu'il aimerait vérifier: plus il fait froid plus les voyageurs sont chargés (manteau, écharppes, gant) plus ils ont donc de probabilité de les oublier. Mais empiler toutes ces couches prend du temps, ce qui pousse aussi à se mettre en retard et dans la précipitation, à oublier d'autres affaires encore. A l'aide des données de la SNCF et d'autres données, essayez de creuser cette piste.

++A partir de l'API open data de la sncf.++

Requeter la base de données des objets trouvés pour récupérer les données entre 2016 et 2021
- Bonus: écrivez un brief permettant d'alimenter chaque jour votre BDD avec les nouvelles données.

++A partir d'internet:++

Récupérer la liste des températures journalières par ville en France entre 2016 et 2021.
++Data analyse VISUALISATION. - (Sur un streamlit)++

Calculez entre 2016 et 2021 la somme du nombre d'objets perdus par semaine. Afficher sur un histogramme la répartition de ces valeurs. (un point correspond à une semaine dont la valeur est la somme).

Afficher l'évolution du nombre d'objets perdus à l'aide d'un plotly sur la période 2016-2021. On peut choisir d'afficher ou non certains types d'objet.

Afficher une carte de France avec le nombre d'objets perdus en fonction de la fréquentation de voyageur de chaque région. Possibilité de faire varier par année et par type d'objets

++Partie data analyse en vue de la DATA SCIENCE. - (sur un notebook)++

Afficher le nombre d'objets perdus en fonction de la température sur un scatterplot Est ce que le nombre d'objets perdus est corrélé à la temperature?

Quelle est la médiane du nombre d'objets perdus en fonction de la saison?

Représenter cette information à l'aide d'un Boxplot. Est ce que le nombre d'objets perdus est corrélé à la saison?

Est ce que le type d'objet perdu est corrélé au mois?
    """)


choice = st.selectbox('Search by :',('day', 'week', 'quarter', 'month', 'year'))




df_weather_by_choice = pd.read_csv(f"CSV/weather_by_dep_by_{choice}.csv")
df_choice_total = pd.read_csv(f'CSV/df_{choice}_total.csv')
df_choice_by_type = pd.read_csv(f'CSV/df_{choice}_by_type.csv')

if choice in ['day', 'week']:
    objet_region_by_choice = pd.read_csv(f'CSV/objects_by_region_by_{choice}.csv')
else :
    objet_region_by_choice = pd.read_csv(f'CSV/objects_by_region_by_{choice}.csv')
    

mygrid2 = make_grid(1,6)
with mygrid2[0][0]:
    st.metric("Lost items", millify(df_choice_total.nb_objets.sum(), precision=2))


with mygrid2[0][1]:
    st.metric(f"Max lost items by {choice} :", millify(df_choice_total.sort_values('nb_objets', ascending=False).iloc[0,1], precision=2))
with mygrid2[0][1]:
    date = str(df_choice_total.sort_values('nb_objets', ascending=False).iloc[0,0]).split(' ',1)[0]
    if choice == 'year':
        st.write(f"In {choice} : {date.split('-', 2)[0]}")
    elif choice == 'month':
        st.write(f"In {choice} : {date.split('-', 2)[1]}")
    else :
        st.write(f"In {date}") 


with mygrid2[0][2]:
    st.metric(f"Min lost items by {choice} :", millify(df_choice_total.sort_values('nb_objets', ascending=True).iloc[0,1], precision=2))
with mygrid2[0][2]:
    date = str(df_choice_total.sort_values('nb_objets', ascending=True).iloc[0,0]).split(' ',1)[0]
    if choice == 'year':
        st.write(f"In {choice} : {date.split('-', 2)[0]}")
    elif choice == 'month':
        st.write(f"In {choice} : {date.split('-', 2)[1]}")
    else :
        st.write(f"In {date}") 

with mygrid2[0][3]:
    st.metric(f"Max temperature by {choice} :", str(round(df_weather_by_choice.sort_values('tc', ascending=False).iloc[0,5],2))+" c")
with mygrid2[0][3]:
    date = str(df_weather_by_choice.sort_values('tc', ascending=False).iloc[0,2]).split(' ',1)[0]
    if choice == 'year':
        st.write(f"In {choice} : {date.split('-', 2)[0]}")
    elif choice == 'month':
        st.write(f"In {choice} : {date.split('-', 2)[1]}")
    else :
        st.write(f"In {date}") 

with mygrid2[0][4]:
    st.metric(f"Min temperature by {choice} :", str(round(df_weather_by_choice.sort_values('tc', ascending=True).iloc[0,5],2))+" c")
with mygrid2[0][4]:
    date = str(df_weather_by_choice.sort_values('tc', ascending=True).iloc[0,2]).split(' ',1)[0]
    if choice == 'year':
        st.write(f"In {choice} : {date.split('-', 2)[0]}")
    elif choice == 'month':
        st.write(f"In {choice} : {date.split('-', 2)[1]}")
    else :
        st.write(f"In {date}") 


with mygrid2[0][5]:
    st.metric(f"Average temperature by {choice} :", str(round(df_weather_by_choice.tc.mean(),2))+" c")

df_departements_weather_by_choice_lat_mean = df_weather_by_choice['lat'].mean()
df_departements_weather_by_choice_long_mean = df_weather_by_choice['long'].mean()

#########################################
#########################################



options_dates = df_weather_by_choice['date'].unique()
choosed_time = st.select_slider(
    f"Choose your {choice}",
    options=options_dates)

st.write(f'Choosed_time : {choosed_time}')


#########################################
#########################################


df_objet_region_by_choice = objet_region_by_choice[objet_region_by_choice['date'] == choosed_time]
df_objet_region_by_choice = df_objet_region_by_choice.fillna(df_objet_region_by_choice.mean())


# initialize the map and store it in a m object
m = folium.Map(location=[df_departements_weather_by_choice_lat_mean, df_departements_weather_by_choice_long_mean], zoom_start=5)
folium.TileLayer('stamentoner').add_to(m) # Sets Tile Theme to (Dark Theme)
folium.Choropleth(geo_data = geo).add_to(m)

choropleth = folium.Choropleth(
    geo_data=geo,
    name="France departements",
    data= df_objet_region_by_choice,
    columns=["region", "n"],
    key_on="feature.properties.nom",
    fill_color="OrRd",  # for more colors : https://github.com/python-visualization/folium/blob/v0.2.0/folium/utilities.py#L104
    nan_fill_color='white',
    fill_opacity=0.7,
    line_opacity=.1,
    overlay=True,
    legend_name="Lost items",
).add_to(m)
#choropleth.geojson.add_to(m)



df_indexed = df_objet_region_by_choice.set_index('region')
for feature in choropleth.geojson.data['features']:
    state_name = feature['properties']['nom']
    feature['properties']['Lost_objects'] = 'Objects Trouvés: ' + '{:,}'.format(df_indexed.loc[state_name, 'n']) if state_name in list(df_indexed.index) else ''
    #feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['nom', 'Lost_objects'], labels=False)
)







#########################################
#########################################


df_weather_by_choice = df_weather_by_choice[df_weather_by_choice['date'] == choosed_time]
df_departements_weather_by_choice = df_weather_by_choice[['lat',	'long'	,'tc']]
df_departements_weather_by_choice = df_departements_weather_by_choice.fillna(df_departements_weather_by_choice.mean())

hm = folium.Map(location=[df_departements_weather_by_choice_lat_mean, df_departements_weather_by_choice_long_mean], 
               tiles='stamentoner',
               zoom_start=5)
HeatMap(df_departements_weather_by_choice, 
        min_opacity=0.4,
        blur = 18
               ).add_to(folium.FeatureGroup(name='Heat Map').add_to(hm))
# folium.LayerControl().add_to(hm)


#########################################
#########################################






with st.expander('\U0001F4CA Histogram and line plots graphics'):
    
    col1, col2 = st.columns(2)



    fig = go.Figure(data=[go.Histogram(nbinsx=20,x=df_choice_total.nb_objets)]).update_layout(
        xaxis_title="N of found aobjects", yaxis_title=f"{choice} from 2016 to 2021", title=go.layout.Title(text=f"Sum of lost items per {choice}")
    )


    fig1 = go.Figure(data=[go.Line(x=df_choice_total.date, y = df_choice_total.nb_objets)]).update_layout(
        xaxis_title=f"{choice} from 2016 to 2021", yaxis_title="N of found aobjects", title=go.layout.Title(text=f"Sum of lost items per {choice}")
    )
    with col1:
        
        st.plotly_chart(fig, use_container_width=True)

        
    with col2:
        
        st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(df_choice_by_type, x=df_choice_by_type.index, y='nb_objets', color='type', hover_name="type")
    st.plotly_chart(fig2, use_container_width=True)


with st.expander('\U0001F30D Folium maps'):
    col3, col4 = st.columns(2)
    with col3:
        st_folium(hm, width=700, height=450)

    with col4:
        st_folium(m, width=700, height=450)
        if choice in ['day', 'week']:
            st.warning('Attention : Brut values presented in this map')