import pandas as pd
import streamlit as st 
import plotly.express as px
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import MarkerCluster


#____________________ Page configuration


st.set_page_config(
    layout='centered',
    initial_sidebar_state='auto'
)

#____________________ Global varibles

current_page = st.session_state.get('current_page', 'Map')
select_comuna = ''
select_barrio = ''
select_cat = ''
new_df = []

#_____________________ Source dataset reading.
# csv_file_path = "/app/oferta_gastronomica (2).csv"  ### Dockers container path
csv_file_path = "https://raw.githubusercontent.com/Remolino777/App_Gastronomica/main/oferta_gastronomica%20(2).csv"
@st.cache_data   #cache the csv file
def load_data(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df

df = load_data(csv_file_path)
new_df = ['id', 'nombre', 'categoria', 'direccion_completa', 'barrio', 'comuna', 'long', 'lat']



load_data(csv_file_path)
#_____________________ New df copy.
df_1 = df[new_df].copy()
df_1.rename(columns={'id':'id_local', 'direccion':'direccion_completa'})
# For markers
dff = df_1[['lat', 'long', 'nombre']].copy()


#_______________________ Maps and markers and tabs

min_lon, max_lon = -58.23, -58.63
min_lat, max_lat = -34.75, -34.50

m = folium.Map(location=[-34.61777, -58.43210], 
            tiles='Esri_WorldGrayCanvas', 
            zoom_control=False, zoom_start=12, min_zoom=12,
            max_bounds=True, # Creation of map's limits.
            min_lat = min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon                  
            )
    


marker_cluster = MarkerCluster().add_to(m)
    


#_______________________________SIDE BAR
with st.sidebar:
    
    st.image('/app/Baires_Logo.png', use_column_width=True)
    select_comuna = st.selectbox('COMUNA',df['comuna'].unique(), index=None, placeholder='Select...')
    
    df_filtered1 = df[df['comuna']==select_comuna]

    if not df_filtered1.empty:    
        select_barrio =st.selectbox('BARRIO',df_filtered1['barrio'].unique(), index=None, placeholder='Select...')    
        select_cat = st.selectbox('CATEGORIA',df['categoria'].drop_duplicates().dropna(), index=None, placeholder='Select...')
        # dff2 = df_filtered1[(df_filtered1['barrio']==select_barrio) & (df_filtered1['categoria']==select_cat)]
        
    else:
        pass  

    

#_________Map Render and mark generator

df_filtered1 = df[df['comuna']==select_comuna]
df_plot = df_filtered1['categoria'].value_counts()
dff2 = df_filtered1[(df_filtered1['barrio']==select_barrio) & (df_filtered1['categoria']==select_cat)]

for i in dff2.index:
            lat = dff2.loc[i, 'lat']
            long = dff2.loc[i, 'long']
            nombre = dff2.loc[i, 'nombre']
            folium.Marker(location=(lat, long),
                popup=nombre,
                tooltip=nombre
                ).add_to(marker_cluster) 
            
st_data = st_folium(m, width=700, height=650)
st.write('Buenos Aires, Argentina') 
