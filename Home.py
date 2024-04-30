import streamlit as st 




st.set_page_config(
    layout='centered',
    initial_sidebar_state='collapsed'
)
col1, col2, col3 = st.columns([1,2,1])
st.divider()
st.divider()
with col1:
    "---"

with col2:
    "---"
    st.image('Baires_Logo.png', use_column_width=True)
    st.divider()
    st.title('Oferta gastronomica 2023 de la ciudad de *Buenos Aires, Argentina*')
    
with col3:
    "---"


with st.sidebar:
    
    st.image('Baires_Logo.png', use_column_width=True) 