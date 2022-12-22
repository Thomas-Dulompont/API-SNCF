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
##########################################
##########################################


st.set_page_config(page_icon=":movie_camera:",
                layout="wide")



#########################################
#########################################

objects_par_regions = pd.read_csv('CSV/objects_par_region.csv')


geo = json.load(open("GEOJSON/regions.geojson")) # lire les données 

#########################################
#########################################



choice = st.selectbox('Search by :',('day', 'week', 'quarter', 'month', 'year'))

df_weather_by_choice = pd.read_csv(f"CSV/weather_by_dep_by_{choice}.csv")
objet_region_by_choice = pd.read_csv(f'CSV/objects_by_region_by_{choice}.csv')

df_departements_weather_by_choice_lat_mean = df_weather_by_choice['lat'].mean()
df_departements_weather_by_choice_long_mean = df_weather_by_choice['long'].mean()

#########################################
#########################################





options_dates = df_weather_by_choice['date'].unique()
choosed_time = st.select_slider(
    f"Choose your {choice}",
    options=options_dates)

st.write(choosed_time)


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





col1, col2 = st.columns(2)






with col1:
    st_folium(hm, width=700, height=450)

with col2:
    st_folium(m, width=700, height=450)#, width=700, height=450)




