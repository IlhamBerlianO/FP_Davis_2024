import streamlit as st
from pathlib import Path
import base64
import matplotlib.pyplot as plt
import pandas as pd
from gtts import gTTS
from deep_translator import GoogleTranslator
import io
import altair as alt
import os
import mysql.connector
from mysql.connector import Error
from streamlit_lightweight_charts import renderLightweightCharts
import plotly.express as px

# Initial page config
st.set_page_config(
     page_title='Final Project Davis 2024',
     layout="wide",
     initial_sidebar_state="expanded",
)

def main():
     data_dipilih = cs_sidebar()
     cs_body((data_dipilih))
     return None

def img_to_bytes(img_path):
     img_bytes = Path(img_path).read_bytes()
     encoded = base64.b64encode(img_bytes).decode()
     return encoded

# Sidebar
def cs_sidebar():
     st.sidebar.markdown("""
               <h1 style='text-align: center; margin-bottom: 40px;'>📈Dashboard📉</h1>
          """, unsafe_allow_html=True)
     data_dipilih = st.sidebar.selectbox("__Select data__", ["Database Dump_AW", "Scrapping IMDB"])
     st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
     return data_dipilih

##########################
# Main body of cheat sheet
##########################
def cs_body(data_dipilih):
     if data_dipilih == "Database Dump_AW":
          # Function to create a connection to the database
          def create_connection():
               try:
                    connection = mysql.connector.connect(
                         host="kubela.id",
                         user="davis2024irwan",
                         passwd="wh451n9m@ch1n3",
                         port=3306,  
                         database="aw"
                    )
                    if connection.is_connected():
                         # st.write("Connection to database was successful")
                         return connection
               except Error as e:
                    print(f"Error: '{e}'")
                    return None
          
          connection = create_connection()

          # Untuk mendapatkan Year unik
          cursor = connection.cursor()
          query = "SELECT DISTINCT CalendarYear FROM dimtime"
          cursor.execute(query)
          unique_years = [row[0] for row in cursor.fetchall()]

          st.sidebar.markdown("""
               <h3 style='text-align: center;'>Filter</h3>
          """, unsafe_allow_html=True)
          filter_database_1= st.sidebar.selectbox("Year:", ["All"] + unique_years)
          st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
          st.sidebar.markdown('''<small>[FP_Davis_2024](https://github.com/IlhamBerlianO/FP_Davis_2024)  | 21082010034 | [Ilham Berlian O](https://github.com/IlhamBerlianO/)</small>''', unsafe_allow_html=True)

          # Judul aplikasi
          st.markdown("""
               <h1 style='text-align: center; margin-bottom: 40px;'>💾Visualization Dump Adventure Work💾</h1>
          """, unsafe_allow_html=True)

          col1, col2, col3 = st.columns([1, 1.5, 1])

          with col1:
               # Query SQL Comparison
               if filter_database_1 == "All":
                    composition = """
                         SELECT 
                              dg.EnglishCountryRegionName AS Country,
                              COUNT(dc.CustomerKey) AS Total_Customers
                         FROM 
                              dimgeography dg
                         JOIN 
                              dimcustomer dc ON dg.GeographyKey = dc.GeographyKey
                         GROUP BY 
                              dg.EnglishCountryRegionName
                    """
                    cursor.execute(composition)
                    # Mengambil hasil query Composition
                    hasil_composition = cursor.fetchall()

               elif filter_database_1:
                    composition = """
                         SELECT 
                              dg.EnglishCountryRegionName AS Country,
                              COUNT(dc.CustomerKey) AS Total_Customers
                         FROM 
                              dimgeography dg
                         JOIN 
                              dimcustomer dc ON dg.GeographyKey = dc.GeographyKey
                         JOIN 
                              factinternetsales fs ON dc.CustomerKey = fs.CustomerKey
                         JOIN 
                              dimtime t ON fs.OrderDateKey = t.TimeKey
                         WHERE 
                              t.CalendarYear = %s
                         GROUP BY 
                              dg.EnglishCountryRegionName
                    """
                    cursor.execute(composition, (filter_database_1,))
                    # Mengambil hasil query Composition
                    hasil_composition = cursor.fetchall()

               # Plot Composition
               data_composition = pd.DataFrame(hasil_composition, columns=['Total_Customers', 'Country']) 
               fig = px.pie(data_composition, values='Total_Customers', names='Country')
               fig.update_layout(
                    title={'text': 'Total Customers by Country', 'font_size': 20, 'font_family': 'Arial'},
                    margin=dict(b=90, t=50, r=10, l=0)
               )

               st.plotly_chart(fig, use_container_width=True)
               
          with col2:
               # Query SQL Comparison
               if filter_database_1 == "All":
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
                    cursor.execute(comparison)
                    # Mengambil hasil query Comparison
                    hasil_comparison = cursor.fetchall()

                    relationship = """
                         SELECT 	
                              f.ProductStandardCost, 
                              f.UnitPrice 
                         FROM 	
                              factinternetsales as f 
                         GROUP BY 	
                              f.ProductStandardCost, f.UnitPrice;
                    """
                    cursor.execute(relationship)
                    # Mengambil hasil query Relationship
                    hasil_relationship = cursor.fetchall()

               elif filter_database_1:
                    comparison = """
                         SELECT 
                              t.MonthNumberOfYear AS Month,
                              SUM(fs.OrderQuantity) AS Total_Order_Quantity 
                         FROM 
                              factinternetsales fs 
                         JOIN 
                              dimtime t ON fs.OrderDateKey = t.TimeKey 
                         WHERE 
                              t.CalendarYear = %s
                         GROUP BY 
                              t.MonthNumberOfYear
                         ORDER BY 
                              t.MonthNumberOfYear;
                    """
                    cursor.execute(comparison, (filter_database_1,))
                    # Mengambil hasil query Comparison
                    hasil_comparison = cursor.fetchall()

                    relationship = """
                         SELECT 
                              f.ProductStandardCost,
                              f.UnitPrice 
                         FROM 
                              factinternetsales as f
                         JOIN 
                              dimtime t ON f.OrderDateKey = t.TimeKey
                         WHERE 
                              t.CalendarYear = %s
                         GROUP BY 
                              f.ProductStandardCost, f.UnitPrice;
                    """
                    cursor.execute(relationship, (filter_database_1,))
                    # Mengambil hasil query Relationship
                    hasil_relationship = cursor.fetchall()

               # Plot Comparison
               data_comparison = pd.DataFrame(hasil_comparison, columns=['Month', 'Total_Order_Quantity'])
               fig = px.line(data_comparison, x='Month', y='Total_Order_Quantity', markers=True)
               fig.update_layout(
               title={'text': 'Total Sales Quantity by Month', 'font_size': 20, 'font_family': 'Arial'},
               xaxis_title='Month',
               yaxis_title='Total Product'
               )
               st.plotly_chart(fig, use_container_width=True)

               # Plot Relationship
               data_relationship = pd.DataFrame(hasil_relationship, columns=['ProductStandardCost', 'UnitPrice'])
               fig = px.scatter(data_relationship, 
                    x='ProductStandardCost', 
                    y='UnitPrice', 
                    hover_data=['ProductStandardCost', 'UnitPrice'],
                    title='Film Gross Revenue',
                    labels={'ProductStandardCost': 'Product Standard Cost', 'UnitPrice': 'Unit Price'}
               )

               fig.update_layout(
                    title={'text': 'Relationship between PSC and PP', 'font_size': 20, 'font_family': 'Arial'},
                    xaxis=dict(showgrid=True, title='Product Standard Cost'),
                    yaxis=dict(showgrid=True, title='Product Price'), 
                    showlegend=False,
                    margin=dict(b=0)
               )

               st.plotly_chart(fig, use_container_width=True)

          with col3:
               # Query SQL Comparison
               if filter_database_1 == "All":
                    distribution = """
                         SELECT 
                              dpc.EnglishProductCategoryName AS Category_Product,
                              COUNT(dp.ProductKey) AS Total_Procut 
                         FROM 
                              dimproductcategory dpc
                         JOIN 
                              dimproductsubcategory dpsc ON dpc.ProductCategoryKey = dpsc.ProductCategoryKey 
                         JOIN
                              dimproduct dp ON dpsc.ProductsubCategoryKey = dp.ProductsubCategoryKey
                         GROUP BY 
                              dpc.EnglishProductCategoryName
                         ORDER BY 
                              dpc.EnglishProductCategoryName;
                    """
                    cursor.execute(distribution)
                    # Mengambil hasil query distribution
                    hasil_distribution = cursor.fetchall()

               elif filter_database_1:
                    distribution = """
                         SELECT 
                              dpc.EnglishProductCategoryName AS Category_Product,
                              COUNT(dp.ProductKey) AS Total_Product 
                         FROM 
                              dimproductcategory dpc
                         JOIN 
                              dimproductsubcategory dpsc ON dpc.ProductCategoryKey = dpsc.ProductCategoryKey 
                         JOIN
                              dimproduct dp ON dpsc.ProductSubcategoryKey = dp.ProductSubcategoryKey
                         JOIN
                              factinternetsales fs ON dp.ProductKey = fs.ProductKey
                         JOIN
                              dimtime t ON fs.OrderDateKey = t.TimeKey 
                         WHERE 
                              t.CalendarYear = %s
                         GROUP BY 
                              dpc.EnglishProductCategoryName
                         ORDER BY 
                              dpc.EnglishProductCategoryName;
                         """
                    cursor.execute(distribution, (filter_database_1,))
                    # Mengambil hasil query Distribution
                    hasil_distribution = cursor.fetchall()

               # Plot Distribution
               data_distribution = pd.DataFrame(hasil_distribution, columns=['Category_Product', 'Total_Procut']) 
               chart1 = alt.Chart(data_distribution).mark_bar().encode(
                    x=alt.X('Category_Product:N', axis=alt.Axis(labelAngle=0, title='Category Product')),
                    y=alt.Y('Total_Procut:Q', axis=alt.Axis(title='Total Product')),
                    tooltip=['Category_Product', 'Total_Procut']
               ).configure_axis(
                    grid=True
               ).interactive().properties(
                    title=alt.TitleParams('First Week Gross Revenue', fontSize=20, fontWeight='bold', font='Arial')
               )

               st.altair_chart(chart1, use_container_width=True)
      
     elif data_dipilih == "Scrapping IMDB":
          # Membaca file excel
          baca = pd.read_excel("scrapping_imdb/top_picks_data.xlsx")

          # Untuk Filter Color
          unique_colors = baca['Color'].unique()

          # Untuk Filter Genre
          data_genres = baca['Genre'].dropna().tolist()
          unique_genres = sorted(set(genre.strip() for sublist in baca['Genre'].dropna().str.split(',') for genre in sublist))
          
          # Untuk Grafik Total Movies by Genre
          split_genres = [genre.strip() for genres in data_genres for genre in genres.split(',')]
          value_unique_genres = pd.Series(split_genres).value_counts()

          st.sidebar.markdown("""
               <h3 style='text-align: center;'>Filter</h3>
          """, unsafe_allow_html=True)
          filter_scrapping_1 = st.sidebar.multiselect('Genres:', unique_genres)
          filter_scrapping_2 = st.sidebar.multiselect('Color:', unique_colors)         
          filter_scrapping_3 = st.sidebar.slider("Rating:", 0.0, 10.0)
          # Filter the data based on the selected filters
          if not filter_scrapping_1 and not filter_scrapping_2:
               filtered_data = baca[baca['Rating'] >= filter_scrapping_3]
          elif not filter_scrapping_1:
               filtered_data = baca[(baca['Color'].isin(filter_scrapping_2)) & (baca['Rating'] >= filter_scrapping_3)]
          elif not filter_scrapping_2:
               filtered_data = baca[(baca['Genre'].str.contains('|'.join(filter_scrapping_1))) & (baca['Rating'] >= filter_scrapping_3)]
          else:
               filtered_data = baca[(baca['Genre'].str.contains('|'.join(filter_scrapping_1))) & (baca['Color'].isin(filter_scrapping_2)) & (baca['Rating'] >= filter_scrapping_3)]

          if not filter_scrapping_1 and not filter_scrapping_2 and filter_scrapping_3 == 0.0:
               filtered_data = baca

          
          st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
          st.sidebar.markdown('''<small>[FP_Davis_2024](https://github.com/IlhamBerlianO/FP_Davis_2024)  | 21082010034 | [Ilham Berlian O](https://github.com/IlhamBerlianO/)</small>''', unsafe_allow_html=True)

          # Judul aplikasi
          st.markdown("""
               <h1 style='text-align: center;'>🎬Visualization IMDB🎬</h1>
          """, unsafe_allow_html=True)

          # Deskripsikan col
          col1, col2, col3 = st.columns([1, 2, 1])

          # Menampilkan konten 
          with col1:
               # First Week Gross Revenue
               fig = px.scatter(baca, 
                    x='Title', 
                    y='Opening_week_rev', 
                    size='Opening_week_rev', 
                    hover_data=['Title', 'Opening_week_rev'],
                    title='Film Gross Revenue',
                    labels={'Title': 'Title', 'Opening_week_rev': 'Opening week rev'},
                    size_max=40)

               fig.update_layout(
                    title={'text': 'First Week Gross Revenue', 'font_size': 20, 'font_family': 'Arial'},
                    xaxis=dict(showgrid=False, showticklabels=False, title='Title'),
                    yaxis=dict(showgrid=True, title='Opening week rev'), 
                    showlegend=False
               )

               st.plotly_chart(fig, use_container_width=True)

               # Total Movies by Genre
               df_plotly = pd.DataFrame({'genre': value_unique_genres.index, 'total_movies': value_unique_genres.values})

               fig = px.pie(df_plotly, values='total_movies', names='genre')
               fig.update_layout(
                    title={'text': 'Total Movies by Genre', 'font_size': 20, 'font_family': 'Arial'},
                    margin=dict(b=90, t=50, r=10, l=0)
               )

               st.plotly_chart(fig,use_container_width=True)

          with col2:
               # Penambahan space agar rapi
               st.write('')
               st.write('')
               # Top 5 Movies
               top5_grossing_films = baca.nlargest(5, 'Gross_us').sort_values(by='Gross_us', ascending=False)
               
               chart1 = alt.Chart(top5_grossing_films).mark_bar().encode(
                    x=alt.X('Gross_us:Q', axis=alt.Axis(title='Gross US ($)')),
                    y=alt.Y('Title:N', sort='-x'),
                    tooltip=['Title', 'Gross_us']
               ).configure_axis(
                    grid=False
               ).interactive().properties(
                    title=alt.TitleParams('Top 5 Movies', fontSize=20, font='Arial')
               )

               st.altair_chart(chart1, use_container_width=True)

               # Total Movies by Year
               baca['Opening_week_date'] = pd.to_datetime(baca['Opening_week_date'])
               baca['Year'] = baca['Opening_week_date'].dt.year
               film_per_year = baca.groupby('Year').size().reset_index(name='Total_Film')
               fig = px.line(film_per_year, x='Year', y='Total_Film', markers=True)
               fig.update_layout(
                    title={'text': 'Total Movies by Year', 'font_size': 20, 'font_family': 'Arial'},
                    xaxis_title='',
                    yaxis_title=''
               )
               st.plotly_chart(fig, use_container_width=True)

          with col3:
               # Penambahan space agar rapi
               st.write('')
               # High/Low Budget
               sorted_data = baca.sort_values(by='Budget', ascending=False)
               top_film = sorted_data.iloc[0]
               low_film = sorted_data.iloc[-1]

               budget_delta = top_film['Budget'] - low_film['Budget']

               st.markdown("""<h3 style='font-size: 20px; font-family: Arial;';>High/Low Budget</h3>""", unsafe_allow_html=True)

               st.metric(label=f"{top_film['Title']}", value=f"${top_film['Budget']:,.2f}", delta=f"${budget_delta:,.2f}")
               st.metric(label=f"{low_film['Title']}", value=f"${low_film['Budget']:,.2f}", delta=f"-${budget_delta:,.2f}")

               # Penambahan agar rapi
               st.write('')

               # Top Rating
               st.markdown("""<h3 style='font-size: 20px; font-family: Arial;';>Top Rating</h3>""", unsafe_allow_html=True)

               data_top_rating = baca[['Title', 'Rating']]
               data_top_rating = data_top_rating.sort_values(by='Rating', ascending=False)
               st.dataframe(
                    data_top_rating,
                    column_config={
                         "Rating": st.column_config.ProgressColumn(
                              "Rating",
                              format="%f",
                              min_value=0,
                              max_value=10
                         )
                    },
                    hide_index=True
               )

               # About
               with st.expander('About Visualization', expanded=False):
                    st.write('''
                         - :orange[**Data**]: [Web IMDB](www.imdb.com).
                         - :orange[**First Week Gross Revenue**]: Total gross revenue of a movies in its first week.
                         - :orange[**Top 5 Movies**]: 5 highest grossing movies.
                         - :orange[**High/Low Budget**]: Movies that have the highest and lowest budgets.
                         - :orange[**Total Movies by Genre**]: Total number of movies by each genre.
                         - :orange[**Total Movies by Year**]: Total number of movies by year.
                         - :orange[**Top Rating**]: The order of movies is based on ratings in order from highest to lowest.
                    ''')
          
          st.markdown('''<hr>''', unsafe_allow_html=True)
        
          # Judul aplikasi
          st.markdown("""
               <h1 style='text-align: center; margin-bottom: 40px;'>Movie List</h1>
          """, unsafe_allow_html=True)
        
          # Folder gambar
          image_folder = "gambar"

          num_cols = 6

          # Menampilkan film berdasarkan filter
          for i in range(0, len(filtered_data), num_cols):
               cols = st.columns(num_cols)
               for j, index in enumerate(range(i, min(i + num_cols, len(filtered_data)))):
                    row = filtered_data.iloc[index]
                    with cols[j]:
                         image_path = os.path.join(image_folder, row['Image'])
                         if os.path.exists(image_path):
                              st.image(image_path, use_column_width=True, caption=row['Title'])
                              st.write(f"Rating: {row['Rating']:.1f}/10.0")
                              # Button Detail of movie
                              if st.button("Detail of movie", key=f"details_{index}"):
                                   st.write(f":orange[**Title :**] {row['Title']}")
                                   st.write(f":orange[**Rating :**] {row['Rating']}/10.0")
                                   st.write(f":orange[**Genre :**] {row['Genre']}")
                                   st.write(f":orange[**Time :**] {row['Runtime']} Minutes")
                                   st.write(f":orange[**Summary :**] {row['Summary']}")

                              # Fungsi untuk merubah teks deskripsi menjadi suara
                              def text_to_speech(text):
                                   tts = gTTS(text=text, lang='en')  
                                   speech = io.BytesIO()
                                   tts.write_to_fp(speech)
                                   return speech.getvalue()
                              
                              # Button Summari in sound
                              if st.button("Summary in sound", key=f"read_{index}"):
                                   speech_bytes = text_to_speech(row['Summary'])
                                   st.audio(speech_bytes, format='audio/mp3')

                              # Button Translate to Indonesian
                              if st.button("Translate to Indonesian", key=f"translate_{index}"):
                                   translator = GoogleTranslator(source='en', target='id')
                                   summary_id = translator.translate(row['Summary'])
                                   st.write(f":orange[**Translated Summary :**] {summary_id}")
                              
                              st.markdown('') # Hanya penambah space saja
                         else:
                              st.markdown("![Image not available](https://via.placeholder.com/150)")
               st.markdown('''<hr>''', unsafe_allow_html=True)

     else:
          st.write("Data yang dipilih tidak tersedia")

     return None

# Run main()
if __name__ == '__main__':
     main()
