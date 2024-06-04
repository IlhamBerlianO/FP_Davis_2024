import streamlit as st
import mysql.connector
from pathlib import Path
import base64
import matplotlib.pyplot as plt

# Menghubungkan ke database MySQL
def connect_to_database():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="dump_aw"
            )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

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
    
    def fetch_data(country=None):
        dataBase = create_connection()
        cursor = dataBase.cursor()
    
        # Query to fetch data
        base_query = """
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
        
        # if country:
        #     query = base_query.format(f"WHERE dst.SalesTerritoryCountry = '{country}'")
        # else:
        #     query = base_query.format("")
    
        cursor.execute(base_query)
        data = pd.DataFrame(cursor.fetchall(), columns=['Month', 'Total_Order_Quantity'])
        col1.markdown(data)
        cursor.close()
        dataBase.close()
        
        
     
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
