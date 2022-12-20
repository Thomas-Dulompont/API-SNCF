import folium
import streamlit as st

from streamlit_folium import st_folium





import json
import pandas as pd

df = pd.read_csv('liste_gares.csv')

geo = json.load(open("departements.geojson")) # lire les données 
# initialize the map and store it in a m object
m = folium.Map(location=[df['latitude_entreeprincipale_wgs84'].mean(), df['longitude_entreeprincipale_wgs84'].mean()], zoom_start=6)

folium.Choropleth(geo_data = geo).add_to(m)

df_departement = df[["departement_libellemin", "code_gare"]]
df_departement = df_departement.groupby('departement_libellemin').aggregate(sum).reset_index()

choropleth = folium.Choropleth(
    geo_data=geo,
    name="France departements",
    data=df_departement,
    columns=["departement_libellemin", "code_gare"],
    key_on="feature.properties.nom",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=.1,
    legend_name="Unemployment Rate (%)",
)
choropleth.geojson.add_to(m)







# https://github.com/zakariachowdhury/streamlit-map-dashboard/blob/main/streamlit_app.py
# call to render Folium map in Streamlit
st_folium(m)#, width=700, height=450)


