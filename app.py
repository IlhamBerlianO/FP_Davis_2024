import streamlit as st
from pathlib import Path
import base64
import mysql.connector
import matplotlib.pyplot as plt

def connect_to_database():
    try:
        # Menghubungkan ke database MySQL menggunakan informasi dari secrets
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["username"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=st.secrets["mysql"]["port"]
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Failed to connect to MySQL: {err}")
        return None

# Initial page config
st.set_page_config(
    page_title='Adventurework Dashboard',
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    conn = connect_to_database()
    if conn is not None:
        cs_sidebar()
        cs_body(conn)
        # Menutup koneksi setelah selesai digunakan
        conn.close()

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
def cs_body(conn):
    col1, col2, col3 = st.columns(3)

    #######################################
    # COLUMN 1
    #######################################
    
    # Comparison (Line Chart)
    col1.subheader('Comparison (Line Chart)')
    col1.markdown('Melihat perkembangan penjualan dari bulan ke bulan.')
    # Membuat kursor untuk eksekusi query SQL
    cursor = conn.cursor()
     
    # Query SQL Comparison
    comparison = """
        SELECT 
            t.MonthNumberOfYear AS Month,
            SUM(fs.OrderQuantity) AS Total_Order_Quantity 
        FROM 
            factinternetsales fs 
        JOIN 
            dimtime t ON fs.OrderDateKey = t.TimeKey 
        GROUP BY 
            t.MonthNumberOfYear
        ORDER BY 
            t.MonthNumberOfYear;
    """
     
    # Eksekusi query
    cursor.execute(comparison)
     
    # Mengambil hasil query
    results = cursor.fetchall()
     
    # Memproses hasil query ke dalam format yang sesuai untuk grafik
    month = []
    total_product_by_month = []
    for row in results:
        month.append(row[0])  
        total_product_by_month.append(row[1])     
     
    # Menampilkan grafik menggunakan widget st.line_chart()
    st.subheader('Comparison (Line Chart)')
    st.markdown('Melihat perkembangan penjualan dari bulan ke bulan.')
    data = {'Month': month, 'Total Product': total_product_by_month}
    line_chart = st.line_chart(data)
     
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
