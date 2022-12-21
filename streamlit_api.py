import folium
import streamlit as st

from streamlit_folium import st_folium





import json
import pandas as pd

df = pd.read_csv('CSV/liste_gares.csv')
df1 = pd.read_csv('CSV/sncf_regions.csv')
geo = json.load(open("GEOJSON/regions.geojson")) # lire les données 
# initialize the map and store it in a m object
m = folium.Map(location=[df['latitude_entreeprincipale_wgs84'].mean(), df['longitude_entreeprincipale_wgs84'].mean()], zoom_start=6)

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




# https://github.com/zakariachowdhury/streamlit-map-dashboard/blob/main/streamlit_app.py
# call to render Folium map in Streamlit
st_folium(m)#, width=700, height=450)


