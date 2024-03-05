import pandas as pd
import streamlit as st 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#____________________ Global varibles

select_comuna = ''

colors = {'RESTAURANTE': '#b6d4bb' , 'BAR':'#f5938b', 'CAFE':'#f0cdab', 'CAFE':'#f1e7c5', 'PUB':'#a6a6a6',\
            'SANDWICHERIA':'#d9ebdd', 'VINERIA':'#b9e6ed', 'CONFITERIA':'#8fcde0', 'DELIVERY & TAKE AWAY':'#619cba'}

colors_1 = ('#b6d4bb' ,'#f5938b', '#f0cdab', '#f1e7c5', '#a6a6a6',
            '#d9ebdd', '#b9e6ed', '#8fcde0', '#619cba')


#_____________________ Source dataset reading.
url = r'D:\0_Respaldo\0_Proyectos_2024\github_projects\Oferta gastronomica\oferta_gastronomica (2).csv'


@st.cache_data   #cache the csv file
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data(url)
new_df = ['id', 'nombre', 'categoria', 'barrio', 'comuna']

#____________________________ New df copy.
df_1 = df[new_df].copy()
#-- Dataframe con la cantidad de 
df_2 = df_1[['comuna','categoria']].copy()
df_3 = df_2[df_2['comuna'] == select_comuna].groupby('categoria').count()  # Group by categoria in the comuna 1
df_3 = df_3.reset_index()
df_3 = df_3.sort_values(by='comuna', ascending=False)
# Buscamos la categoria que mas hay en la zona y la cantidad



#_______________________________SIDE BAR
with st.sidebar:
    
    st.image('Baires_Logo.png', use_column_width=True)
    select_comuna = st.selectbox('COMUNA',df['comuna'].unique(), index=None, placeholder='Select...')
    

if select_comuna:
    # ______________________________QUERY
    df_3 = df_2[df_2['comuna'] == select_comuna].groupby('categoria').count().reset_index()
    df_3 = df_3.sort_values(by='comuna', ascending=False)
    
    
    #_______________________________CHARTS BARS
    fig_1 = px.bar(df_3, x='categoria', y='comuna', labels={'comuna': 'Cantidad de establecimientos'}, \
                                                    color_discrete_map=colors, title='Distribución por categoría',\
                                                          color='categoria', width=850, height=300)
    fig_1.update_layout(margin=dict(l=5, r=5, t=30, b=1)) # Margin adjustment
    st.plotly_chart(fig_1)
    #_______________________________CHARTS PROPORCIONS VS RESTAURANT
    
    t_columnas = len(df_3['comuna'])
    
    fig = make_subplots(rows=1, cols=t_columnas,
                    specs=[[{"type": "domain"}] * t_columnas
                            ])
    
    for i in range(t_columnas):
        categoria = df_3['categoria'].iloc[i]
        if categoria != 'RESTAURANTE':
            fig.add_trace(go.Pie(values=df_3['comuna'].iloc[[0, i]], 
                                labels=df_3['categoria'].iloc[[0, i]], 
                                textinfo='value',
                                marker=dict(colors=[colors_1[0], colors_1[i]])),  
                        row=1, col=i + 1)

   
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=1),
                      title='Proporcion de restaurantes frente otras categorias') # Margin adjustment
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.write("Seleccione una comuna para ver los gráficos.")
    