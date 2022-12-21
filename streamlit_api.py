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
##########################################
##########################################


st.set_page_config(page_icon=":movie_camera:",
                layout="wide")



#########################################
#########################################


df = pd.read_csv('CSV/liste_gares.csv')
df1 = pd.read_csv('CSV/sncf_regions.csv')
geo = json.load(open("GEOJSON/regions.geojson")) # lire les données 

#########################################
#########################################



choice = st.selectbox('Search by :',('day', 'week'))

df_weather_by_choice = pd.read_csv(f"CSV/weather_by_dep_by_{choice}.csv")

df_departements_lat_mean = df_weather_by_choice['lat'].mean()
df_departements_long_mean = df_weather_by_choice['long'].mean()

#########################################
#########################################


# initialize the map and store it in a m object
m = folium.Map(location=[df_departements_lat_mean, df_departements_long_mean], zoom_start=5)
folium.Choropleth(geo_data = geo).add_to(m)

choropleth = folium.Choropleth(
    geo_data=geo,
    name="France departements",
    data=df1,
    columns=["region", "n_objets"],
    key_on="feature.properties.nom",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=.1,
    legend_name="Unemployment Rate (%)",
)
choropleth.geojson.add_to(m)



df_indexed = df1.set_index('region')
for feature in choropleth.geojson.data['features']:
    state_name = feature['properties']['nom']
    feature['properties']['Lost_objects'] = 'Objects Trouvés: ' + '{:,}'.format(df_indexed.loc[state_name, 'n_objets']) if state_name in list(df_indexed.index) else ''
    #feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['nom', 'Lost_objects'], labels=False)
)







#########################################
#########################################

if choice == 'day': 
    steps = timedelta(days=1)
elif choice == "week":
    steps = timedelta(weeks=1)

start_time = st.slider(
    f"Choose your {choice}",
    value=datetime(2016, 12, 12),
    min_value = datetime(2016,1,1),  
    max_value=  datetime(2021,12,12), 
    step= steps,
    format="YYYY-DD-MM")

st.write(str(start_time.date()))

df_weather_by_choice = df_weather_by_choice[df_weather_by_choice['date'] == str(start_time.date())]
df_departements = df_weather_by_choice[['lat',	'long'	,'tc']]
df_departements = df_departements.fillna(df_departements.mean())

hm = folium.Map(location=[df_departements_lat_mean, df_departements_long_mean], 
               tiles='stamentoner',
               zoom_start=5)
HeatMap(df_departements, 
        min_opacity=0.4,
        blur = 18
               ).add_to(folium.FeatureGroup(name='Heat Map').add_to(hm))
# folium.LayerControl().add_to(hm)


#########################################
#########################################





col1, col2 = st.columns(2)






with col1:
    st_folium(hm, width=700, height=450)

with col2:
    st_folium(m, width=700, height=450)#, width=700, height=450)




