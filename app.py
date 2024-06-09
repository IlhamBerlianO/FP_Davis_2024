import streamlit as st
from pathlib import Path
import base64
import matplotlib.pyplot as plt
import pandas as pd
from gtts import gTTS
from deep_translator import GoogleTranslator
import io
import base64

def main():
    data_dipilih = cs_sidebar()
    cs_body(data_dipilih)
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
    data = ["Database Dump_AW", "Scrapping IMDB"]
    data_dipilih = st.sidebar.selectbox("__Pilih data__", data)

    return data_dipilih

##########################
# Main body of cheat sheet
##########################
def cs_body(data_dipilih):
    if data_dipilih == "Database Dump_AW":
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
        

    elif data_dipilih == "Scrapping IMDB":
        st.subheader("Scrapping IMDB")
        st.write("Ini adalah contoh konten yang akan ditampilkan jika Database Dump_AW dipilih.")

    else:
        st.write("Data yang dipilih tidak tersedia")
        

    return None
    
##########################
# Run main()
##########################
if __name__ == '__main__':
    main()
