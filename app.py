import streamlit as st
from pathlib import Path
import base64
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
from st_files_connection import FilesConnection

# # Initialize connection.
# conn = st.connection('mysql', type='sql')

# # Perform query.
# df = conn.query('SELECT * from mytable;', ttl=600)

# # Print results.
# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")
# ======================================
@st.cache_resource
def init_connections():
    return mysql.connector.connect(**st.secrets["mydb"])

conn = init_connections()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * FROM mytable")

for row in rows:
    st.write(f"{row[0]} has a: {row[1]}")
# ======================================
# conn = st.connection('gcs', type=FilesConnection)
# df = conn.read("streamlit-bucket-fp/myfile.csv", input_format="csv", ttl=600)

def main():
    cs_sidebar()
    cs_body()

    return None

# def img_to_bytes(img_path):
#     img_bytes = Path(img_path).read_bytes()
#     encoded = base64.b64encode(img_bytes).decode()
#     return encoded
    
##########################
# SIDEBAR
##########################
def cs_sidebar():
    # st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=32 height=32>](https://streamlit.io/)'''.format(img_to_bytes("logomark_website.png")), unsafe_allow_html=True)
    st.sidebar.header('Adventurework Dashboard')
    tahun = list(range(2019, 2025))
    tahun_dipilih = st.sidebar.selectbox("__Pilih tahun__", tahun)

    return None

##########################
# Main body of cheat sheet
##########################
def cs_body():
    col1, col2, col3 = st.columns(3)
    
    #######################################
    # COLUMN 1
    #######################################
    
    # Comparison (Line Chart)
    col1.subheader('Comparison (Line Chart)')
    col1.markdown('Melihat perkembangan penjualan dari bulan ke bulan.')

    # Perlu? 1
    col1.subheader('Percobaan')

    #######################################
    # COLUMN 2
    #######################################

    # Display interactive widgets
    col2.subheader('Display interactive widgets')
    
    #######################################
    # COLUMN 3
    #######################################

    # Connect to data sources
    col3.subheader('Connect to data sources')
    
    return None
    
##########################
# Run main()
##########################
if __name__ == '__main__':
    main()
