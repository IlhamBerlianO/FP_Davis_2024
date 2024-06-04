import streamlit as st
import mysql.connector
from pathlib import Path
import base64
import matplotlib.pyplot as plt
import pandas as pd

# Initial page config
st.set_page_config(
    page_title='Adventurework Dashboard',
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    cs_sidebar()
    cs_body()

    return None

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
    
##########################
# SIDEBAR
##########################
def cs_sidebar():
    st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=32 height=32>](https://streamlit.io/)'''.format(img_to_bytes("logomark_website.png")), unsafe_allow_html=True)
    st.sidebar.header('Adventurework Dashboard')
    tahun = list(range(2019, 2025))
    tahun_dipilih = st.sidebar.selectbox("__Pilih tahun__", tahun)

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

   #  # Membuat koneksi ke database
   #  def create_connection():
   #      conn = mysql.connector.connect(
   #          host="localhost",
   #          user="root",
   #          password="",
   #          database="dump_aw"
   #      )
   #      return conn
    
   # # Fungsi untuk menjalankan query ke database
   #  def run_query(query):
   #      conn = create_connection()
   #      cursor = conn.cursor()
   #      cursor.execute(query)
   #      result = cursor.fetchall()
   #      conn.close()
   #      return result

    engine = create_engine("mysql://username@localhost/dump_aw")

    result = engine.execute("""
        SSELECT 
            t.MonthNumberOfYear AS Month,
            SUM(fs.OrderQuantity) AS Total_Order_Quantity 
        FROM 
            factinternetsales fs 
        JOIN 
            dimtime t ON fs.OrderDateKey = t.TimeKey 
        GROUP BY 
            t.MonthNumberOfYear
        ORDER BY 
            t.MonthNumberOfYear;""").fetchall()
    
    # Query SQL Comparison
    # comparison = """
    #     SELECT 
    #         t.MonthNumberOfYear AS Month,
    #         SUM(fs.OrderQuantity) AS Total_Order_Quantity 
    #     FROM 
    #         factinternetsales fs 
    #     JOIN 
    #         dimtime t ON fs.OrderDateKey = t.TimeKey 
    #     GROUP BY 
    #         t.MonthNumberOfYear
    #     ORDER BY 
    #         t.MonthNumberOfYear;
    # """
    
    # # Menjalankan query dan mendapatkan hasilnya
    # result1 = run_query(comparison)
    
    # # Menampilkan data di Streamlit
    # st.write(result)
    st.write(result)
     
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

##########################
# Run main()
##########################
if __name__ == '__main__':
    main()
