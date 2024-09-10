import streamlit as st
from appMops import mainMops
from appIps import mainJunos

#st.sidebar.image('proconty.png')
#st.sidebar.title("Pasos a Producción")
menuPrincipal = st.sidebar.radio('Menu Principal', ['Información','1. Junos', '2. Mops'])

if menuPrincipal == 'Información':
    st.title("Pasos a Producción")
    st.write("""Seleccionar en el Menu Principal, una de las siguientes opciones:""")
    st.subheader(' 1. Junos ')
    st.markdown('**:red[Archivo CSV - JUNOS:]**')
    st.write('Permite generar el archivo .csv para cargar las IPs maliciosas en el FW Atlas')
    st.markdown('**:red[Archivo CSV JUNOS - GRUPO:]**')
    st.write('Permite generar el archivo .csv para cargar las IPs maliciosas en el FW Atlas, con la opción de colocar el grupo al cual se desea cargar')
    st.markdown('**:red[Comparación de IPs - JUNOS:]**')
    st.write('Permite comparar las nuevas IPs de Ingeniera con la base de datos del FW Atlas')
    
    st.subheader('2. Mops ')
    st.write('Permite generar MOPs genéricos para la gestión por parte de N2 o Proveedores')
    st.markdown('**:red[MOP Gestión N2 - Generico]**')
    st.markdown('**:red[MOP Proveedor - Generico]**')
    st.markdown('**:red[MOP Preaprobadas]**')
        
elif menuPrincipal == '1. Junos':
    #st.sidebar.text("JUNOS")
    st.title('[Archivo CSV para IPs Maliciosas]')
    mainJunos()
    
elif menuPrincipal == '2. Mops':
    #st.sidebar.text("MOPS")
    st.title('[MOPs Gestión - Preaprobadas]')
    mainMops()

#st.sidebar.write('All rights reserved. Developed by **:blue[David Minango]**')
        
