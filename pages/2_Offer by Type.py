import pandas as pd
import streamlit as st 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#____________________ Global varibles

select_categoria = ''

colors_c = ('#e76578', '#e8878c', '#9c546c', '#c9b4c4', '#82736d', '#658ce7', '#e7de65',
            '#b4c9be', '#c9c1b4', '#8790e8', '#e8e587', '#54849c', '#9c9054', '#8eb1cc', '#8eb1cc')
base_color = '#b6d4bb'


#_____________________ Source dataset reading.
url = r'D:\0_Respaldo\0_Proyectos_2024\github_projects\Oferta gastronomica\oferta_gastronomica (2).csv'


@st.cache_data   #cache the csv file
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data(url)
new_df = ['id','categoria', 'comuna']

#____________________________ New df copy.
df_1 = df[new_df].copy()
df_1 = df_1.dropna()
#-- Dataframe con la cantidad de 
df_2 = df_1[['comuna','categoria']].copy()


#_______________________________SIDE BAR
with st.sidebar:
    
    st.image('Baires_Logo.png', use_column_width=True)
    select_categoria = st.selectbox('CATEGORIA',df_1['categoria'].unique(), index=None, placeholder='Select...')
    

if select_categoria:
    
    # ______________________________QUERY
    df_3 = df_1[df_1['categoria'] == select_categoria].groupby('comuna').count()   # Group by comuna 
    df_3 = df_3.sort_values(by='categoria', ascending=False)
    
    df_3 = df_3.reset_index()

    df_3['Ranking'] = range(1, len(df_3)+1)  #Ranking by categoria

    df_4 = df_3[['Ranking','comuna']]
    
    comuna_top = df_4.iloc[0]['comuna']
    categoria_top = df_3[df_3['comuna'] == comuna_top]['categoria'].values[0]
    
    #_______________________________TITLE HEADER

    st.header(f'La :green[{comuna_top}] es la que tiene mas "{select_categoria}S"', divider='green')
    
    #_______________________________CHARTS BARS
    col1,col2 = st.columns([1,3])
    
    
    with col1:    
        fig_1 = go.Figure(data=[go.Table(
        header=dict(values=['Comuna', 'Ranking'],
                    font=dict(size=18), height=32),
        
        cells=dict(values=[df_3['comuna'], df_3['Ranking']], 
                font=dict(size=14), height=32)
        )])
        fig_1.update_layout(height=1000, width=200, margin=dict(r=30))
        st.plotly_chart(fig_1)
    
    with col2:           
        
        st.subheader(f'Relacion de {select_categoria}S por Comuna Vs _{comuna_top}_')
        
        fig2 = make_subplots(rows=5, cols=3,
                    specs=[[{"type": "domain"}] * 3] * 5)
         
        for i in range(15):
    # Calcular el índice de fila y columna
            row_index = i // 3 + 1
            col_index = i % 3 + 1
            
            # Asegurarse de que no exceda el número total de subplots
            if i < len(df_3):
                comuna = df_3['comuna'].iloc[i]
                if comuna != df_4['comuna'].iloc[0]:  # Comparar con la comuna líder
                    fig2.add_trace(go.Pie(values=[df_3['categoria'].iloc[i], categoria_top], 
                                labels=[df_3['comuna'].iloc[i], comuna_top],
                                marker=dict(colors=[colors_c[i], base_color]),
                                textinfo='value',
                                textfont=dict(size=14),
                                domain={'x':[0,1], 'y':[0,1]}),  
                                row=row_index, col=col_index)
            else:
                # Si se agotan las filas de datos, crear un subplot vacío
                fig2.add_trace(go.Pie(values=[], labels=[], textinfo='value', 
                                     marker=dict(colors=[])), row=row_index, col=col_index)
                
        fig2.update_layout(height=700, margin=dict(l=30), font=dict(size=25))  # Hight adjustment
        st.plotly_chart(fig2, use_container_width=True)       
        
else:
    st.write("Selecciona una categoria para ver los gráficos.")