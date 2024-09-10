#### BIBLIOTECAS ####
import streamlit as st
import docx2txt
#import pdfplumber
from datetime import datetime, date

#UTILS
import base64
import time
timestr = time.strftime("%Y%m%d")
import pandas as pd



class FileDownloader(object):
    def __init__(self, data,filename='JUNOS_CRQ',file_ext='txt'):
        super(FileDownloader, self).__init__()
        self.data = data
        self.filename = filename
        self.file_ext = file_ext

    def download(self):
        b64 = base64.b64encode(self.data.encode()).decode()
        new_filename = "{}_{}_.{}".format(self.filename,timestr,self.file_ext)
        st.markdown("#### Download File ###")
        href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Click Here!!</a>'
        st.markdown(href,unsafe_allow_html=True)



def mainJunos():
    #st.title("Pasos a Producción")

    ### INFORMACION LADO IZQUIERDO ###
    #st.sidebar.image('proconty.jpg', width=300)


    ### ESTRUCTURA PRINCIPAL ### 
    st.title('IPs MALICIOSAS - JUNOS')

    menu = ['Archivo CSV - JUNOS','Archivo CSV JUNOS - GRUPO', 'Comparación de IPs - JUNOS']
    choice = st.sidebar.selectbox('Menu - JUNOS', menu)

    #st.sidebar.markdown('[MENU PRINCIPAL](https://proconty-pap.herokuapp.com/)')

    if choice == 'Archivo CSV - JUNOS':
        st.write('Indicaciones de uso:')
        st.write("Cargar el archivo (.txt), ingresar el número de CRQ y verificar que la fecha este correcta.")
        st.write("Al presionar el boton GENERAR se creara un archivo con el formato para JUNOS.")
        st.write("En la opcion Menu seleccionar el tipo de archivo que desea descargar (.txt o .csv)")
        st.warning("Al abrirse la opcion de descargar colocar el número de CRQ")

        ### CARGAR Y VISUALIZAR ARCHIVO ###
        docx_file = st.file_uploader('Cargar archivo .txt', type=['pdf','docx','txt'])
        if docx_file is not None:

            if docx_file.type == "text/plain":
                # Read as string (decode bytes to string)
                raw_text = str(docx_file.read(),"utf-8")
                st.text(raw_text)
            else:
                raw_text = docx2txt.process(docx_file)
                st.write(raw_text)

        ### INGRESAR CRQ Y FECHA ###
        crq_num = st.text_input('Ingrese el número de la CRQ: ')
        st.write("CRQ_"+crq_num)
        day = date.today().strftime("%A")
        day = day[0:3]
        fecha = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        st.write(day+', '+fecha)

        ##### GENERAR ARCHIVO TXT #####
        def Convert(string):
            li = list(string.split('\n'))
            return li

        if st.button('GENERAR'):
            bandera = Convert(raw_text)
            documento = 'prueba.txt'
            with open(documento, 'w') as f:
                f.write("#Rows which start with '#' are treated as a commented row \n")
                f.write("# \n")
                f.write('\n')
                fechaCreacion = str('#Created time:,'+'"{}'.format(day)+", {}".format(fecha)+'"\n')
                f.write(''.join(fechaCreacion))
                f.write('#Version -11.4 \n')
                f.write('\n')
                f.write("# \n")
                f.write("# \n")
                f.write("# \n")
                f.write('\n')
                f.write('#Start  - Please do not modify or change this line \n')
                f.write('\n')
                f.write('#Section Start - Network Address - Please do not modify or change this line \n')
                f.write('#Explanation for the Column Names \n')
                f.write('# \n')
                f.write('#Name                  - Name of the Address \n')
                f.write('#Domain                - Domains for the Address to be created \n')
                f.write('#Description           - Description for Address \n')
                f.write('#Type                  - Type of the Address. Values can be Network, IPRange or Host \n')
                f.write("#IP Address            - Ip Address(IPv4/IPv6) of the individual host. This field with 'Type' as Host or Network. It can be wildcard ip as well \n")
                f.write('#Subnet Mask/Prefix           - Subnet mask/prefix provided for the IP Address((IPv4/IPv6)) provided in previous column when Type is selected as Network \n')
                f.write('#IP Range Min          - Minimum IP(IPv4) Range in case range is provided. This should be provided when Type is Range \n')
                f.write('#IP Range Max          - Maximum IP(IPv4) Range in case range is provided. This should be provided when Type is Range \n')
                f.write('#Host                  - Host Name of the host address. This should be provided when Type is Host. This field will be ignored if IP Address is provided  \n')
                f.write('#Wildcard Mask         - Wildcard mask IP address (IPV4/IPV6) \n')
                f.write('#Address Groups       - Provide the Address Groups for the Address to be created. \n')
                f.write('#                           If Address Group is not present it would be created. \n')
                f.write("#                           More than one Address Groups should be seperated by '|' \n")
                f.write('#Metadata   - Add metadata with Logical Operatos to your Address. \n')
                f.write('#DnsAddressType        - Type of the DNS Address. Values can be ipv4-only or ipv6only \n')
                f.write('# \n')
                f.write('#Name, Description, Type, IP Address, Subnet Mask/Prefix, IP Range Min, IP Range Max, Host, Wildcard Mask, Address Groups, Metadata, DnsAddressType, Domain \n')
                ipsMali = []
                count = 0
                for line in bandera:
                    if count != len(bandera):
                        ipsMali = str("Host_{}".format(line.strip())+',"CRQ{}",'.format(crq_num)+'Host,'+'{}'.format(line.strip())+',,,,,,,,,,'+'Global/FW_ATLAS')
                        f.write(''.join(ipsMali))
                        f.write('\n')
                        print(ipsMali)
                    else:
                        break
                    count =+ 1

                f.write('\n')
                f.write('#Section End - Network Address - Please do not modify or change this line \n')
                f.write('#End  - Please do not modify or change this line')

        #### DESCARGAR #####
        menu = ['Text', 'CSV']
        choice = st.selectbox('Menu', menu)

        if choice == 'Text':
            if st.button('Guardar TXT'):
                with open('prueba.txt', 'r') as file:
                    dataIPS = file.read()
                    download = FileDownloader(dataIPS).download()

        if choice == 'CSV':
            if st.button('Guardar CSV'):
                with open('prueba.txt', 'r') as file:
                    dataIPScsv = file.read()
                    download = FileDownloader(dataIPScsv, file_ext='csv').download()


        #st.write('All rights reserved. Developed by David Minango')
        
    if choice == 'Archivo CSV JUNOS - GRUPO':
        st.write('Indicaciones de uso:')
        st.write("Cargar el archivo (.txt), ingresar el número de CRQ y verificar que la fecha este correcta.")
        st.write("Al presionar el boton GENERAR se creara un archivo con el formato para JUNOS.")
        st.write("En la opcion Menu seleccionar el tipo de archivo que desea descargar (.txt o .csv)")
        st.warning("Al abrirse la opcion de descargar colocar el número de CRQ")

        ### CARGAR Y VISUALIZAR ARCHIVO ###
        docx_file = st.file_uploader('Cargar archivo .txt', type=['pdf','docx','txt'])
        if docx_file is not None:

            if docx_file.type == "text/plain":
                # Read as string (decode bytes to string)
                raw_text = str(docx_file.read(),"utf-8")
                st.text(raw_text)
            else:
                raw_text = docx2txt.process(docx_file)
                st.write(raw_text)

        ### INGRESAR CRQ Y FECHA ###
        crq_num = st.text_input('Ingrese el número de la CRQ: ')
        st.write("CRQ_"+crq_num)
        day = date.today().strftime("%A")
        day = day[0:3]
        fecha = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        st.write(day+', '+fecha)
        grupoIPs = st.text_input('Ingrese el número del grupo de IPs Públicas Maliciosas')
        st.write('IPs_Publicas_Maliciosas_'+grupoIPs)

        ##### GENERAR ARCHIVO TXT #####
        def Convert(string):
            li = list(string.split('\n'))
            return li

        if st.button('GENERAR'):
            bandera = Convert(raw_text)
            documento = 'prueba.txt'
            with open(documento, 'w') as f:
                f.write("#Rows which start with '#' are treated as a commented row \n")
                f.write("# \n")
                f.write('\n')
                fechaCreacion = str('#Created time:,'+'"{}'.format(day)+", {}".format(fecha)+'"\n')
                f.write(''.join(fechaCreacion))
                f.write('#Version -11.4 \n')
                f.write('\n')
                f.write("# \n")
                f.write("# \n")
                f.write("# \n")
                f.write('\n')
                f.write('#Start  - Please do not modify or change this line \n')
                f.write('\n')
                f.write('#Section Start - Network Address - Please do not modify or change this line \n')
                f.write('#Explanation for the Column Names \n')
                f.write('# \n')
                f.write('#Name                  - Name of the Address \n')
                f.write('#Domain                - Domains for the Address to be created \n')
                f.write('#Description           - Description for Address \n')
                f.write('#Type                  - Type of the Address. Values can be Network, IPRange or Host \n')
                f.write("#IP Address            - Ip Address(IPv4/IPv6) of the individual host. This field with 'Type' as Host or Network. It can be wildcard ip as well \n")
                f.write('#Subnet Mask/Prefix           - Subnet mask/prefix provided for the IP Address((IPv4/IPv6)) provided in previous column when Type is selected as Network \n')
                f.write('#IP Range Min          - Minimum IP(IPv4) Range in case range is provided. This should be provided when Type is Range \n')
                f.write('#IP Range Max          - Maximum IP(IPv4) Range in case range is provided. This should be provided when Type is Range \n')
                f.write('#Host                  - Host Name of the host address. This should be provided when Type is Host. This field will be ignored if IP Address is provided  \n')
                f.write('#Wildcard Mask         - Wildcard mask IP address (IPV4/IPV6) \n')
                f.write('#Address Groups       - Provide the Address Groups for the Address to be created. \n')
                f.write('#                           If Address Group is not present it would be created. \n')
                f.write("#                           More than one Address Groups should be seperated by '|' \n")
                f.write('#Metadata   - Add metadata with Logical Operatos to your Address. \n')
                f.write('#DnsAddressType        - Type of the DNS Address. Values can be ipv4-only or ipv6only \n')
                f.write('# \n')
                f.write('#Name, Description, Type, IP Address, Subnet Mask/Prefix, IP Range Min, IP Range Max, Host, Wildcard Mask, Address Groups, Metadata, DnsAddressType, Domain \n')
                ipsMali = []
                count = 0
                for line in bandera:
                    if count != len(bandera):
                        ipsMali = str("Host_{}".format(line.strip())+',"CRQ{}",'.format(crq_num)+'Host,'+'{}'.format(line.strip())+',,,,,,'+'IPs_Publicas_Maliciosas_{}'.format(grupoIPs)+',,,'+'Global/FW_ATLAS')
                        f.write(''.join(ipsMali))
                        f.write('\n')
                        print(ipsMali)
                    else:
                        break
                    count =+ 1

                f.write('\n')
                f.write('#Section End - Network Address - Please do not modify or change this line \n')
                f.write('#End  - Please do not modify or change this line')

        #### DESCARGAR #####
        menu = ['Text', 'CSV']
        choice = st.selectbox('Menu', menu)

        if choice == 'Text':
            if st.button('Guardar TXT'):
                with open('prueba.txt', 'r') as file:
                    dataIPS = file.read()
                    download = FileDownloader(dataIPS).download()

        if choice == 'CSV':
            if st.button('Guardar CSV'):
                with open('prueba.txt', 'r') as file:
                    dataIPScsv = file.read()
                    download = FileDownloader(dataIPScsv, file_ext='csv').download()


        #st.write('All rights reserved. Developed by David Minango')

    if choice == 'Comparación de IPs - JUNOS':
        st.write('Indicaciones de uso:')
        st.write("Cargar los dos archivos en (.txt), el archivo 1 debe ser la base de datos de JUNOS, el archivo 2 debe ser el enviado por Ingenieria.")
        st.write("Al presionar el boton COMPARAR se generara una tabla con las ips no encontradas en la base de datos de JUNOS.")

        ### CARGAR Y VISUALIZAR ARCHIVO  BASE DE DATOS###
        upload_baseDatos = st.file_uploader('Base de Datos')
        upload_ingenieria = st.file_uploader('Ingenieria')
        if upload_baseDatos:
            df1 = pd.read_table(upload_baseDatos, delimiter=" ", header=None)
            df1 = pd.DataFrame(df1.values, columns=['BaseDatos'])
        #st.write(df1)
        if upload_ingenieria:
            df2 = pd.read_table(upload_ingenieria, header=None)
            df2 = pd.DataFrame(df2.values, columns=['BaseIngenieria'])
            df2 = df2.drop_duplicates()

        unir = st.checkbox('Unir archivos')
        if unir:
            unionDataFrames = pd.concat([df1,df2], axis=1)
            st.write(unionDataFrames)
                     
        if st.button('Comparar'):
            df_1notin2 = df2[~(df2['BaseIngenieria'].isin(df1['BaseDatos']) )].reset_index(drop=True)
            st.write(df_1notin2)

        #st.write('All rights reserved. Developed by David Minango')



