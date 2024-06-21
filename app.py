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
from sqlalchemy import create_engine

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
          database_host = st.secrets["database"]["host"]
          database_username = st.secrets["database"]["username"]
          database_password = st.secrets["database"]["password"]
          database_port = st.secrets["database"]["port"]
          database_name = st.secrets["database"]["database"]

          # Use the credentials to connect to your database
          conn_string = f"mysql://{database_username}:{database_password}@{database_host}:{database_port}/{database_name}"
          engine = create_engine(conn_string, isolation_level="AUTOCOMMIT")

          conn = engine.connect()

          # Untuk mendapatkan Year unik
          cursor = conn.cursor()
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
               <h1 style='text-align: center; margin-bottom: 40px;'>💾Visualization Dump AW💾</h1>
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
               data_composition = pd.DataFrame(hasil_composition, columns=['Country', 'Total_Customers'])

               fig = px.pie(data_composition, values='Total_Customers', names='Country')
               fig.update_layout(
                    title={'text': 'Total Customers by Country', 'font_size': 20, 'font_family': 'Arial'}
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

               # Plot Comparison
               data_comparison = pd.DataFrame(hasil_comparison, columns=['Month', 'Total_Order_Quantity'])
               fig = px.line(data_comparison, x='Month', y='Total_Order_Quantity', markers=True)
               fig.update_layout(
                    title={'text': 'Total Sales Quantity by Month', 'font_size': 20, 'font_family': 'Arial'},
                    xaxis_title='Month',
                    yaxis_title='Total Product'
               )
               st.plotly_chart(fig, use_container_width=True)

          with col3:
               # Query SQL Comparison
               if filter_database_1 == "All":
                    distribution = """
                         SELECT 
                              dpc.EnglishProductCategoryName AS Category_Product,
                              COUNT(dp.ProductKey) AS Total_Product 
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
               data_distribution = pd.DataFrame(hasil_distribution, columns=['Category_Product', 'Total_Product']) 
               chart1 = alt.Chart(data_distribution).mark_bar().encode(
                    x=alt.X('Category_Product:N', axis=alt.Axis(labelAngle=0, title='Category Product')),
                    y=alt.Y('Total_Product:Q', axis=alt.Axis(title='Total Product')),
                    tooltip=['Category_Product', 'Total_Product']
               ).configure_axis(
                    grid=True
               ).interactive().properties(
                    title=alt.TitleParams('Total Product by Category Product', fontSize=20, fontWeight='bold', font='Arial')
               )

               st.altair_chart(chart1, use_container_width=True)
      
          colsatu, coldua = st.columns([2.5,1])
          with colsatu:
               # Query SQL Comparison
               if filter_database_1 == "All":
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

               # Plot Relationship
               data_relationship = pd.DataFrame(hasil_relationship, columns=['ProductStandardCost', 'UnitPrice'])
               fig = px.scatter(data_relationship, 
                    x='ProductStandardCost', 
                    y='UnitPrice', 
                    hover_data=['ProductStandardCost', 'UnitPrice'],
                    title='Relationship between Product Standard Cost and Product Price',
                    labels={'ProductStandardCost': 'Product Standard Cost', 'UnitPrice': 'Unit Price'}
               )

               fig.update_layout(
                    title={'text': 'Relationship Product Standard Cost and Product Price', 'font_size': 20, 'font_family': 'Arial'},
                    xaxis=dict(showgrid=True, title='Product Standard Cost'),
                    yaxis=dict(showgrid=True, title='Product Price'), 
                    showlegend=False
               )

               st.plotly_chart(fig, use_container_width=True)

          with coldua:
               # About
               with st.expander('About Visualization', expanded=False):
                    st.write('''
                         - :orange[**Data**]: The data used is from the Dump Adventure Work database.
                         - :orange[**Total Customers by Country**]: This graph shows the proportion of customers in each country. The graph shows that the United States has the highest number of subscribers, at around 42.3%, followed by Australia with the second highest number of subscribers, at around 19.4%. The country with the lowest number of customers is Canada, which is only 8.5%
                         - :orange[**Total Sales Quantity by Month**]: This graph displays total product sales per month. It can be seen from the graph that the 5th and 6th months had the highest total product sales, namely 6.064 products sold in the 5th month and 6.080 products sold in the 6th month. However, there was a significant decrease in the 7th month where the products only 4.019 were sold.
                         - :orange[**Total Product by Category Product**]: This graph shows the number of products in each category. From the graph, it can be seen that the category with the highest number of products is the Bicycle category, with 116 products. The Accessories and Clothing categories have almost the same number of products, namely 22 products in the Accessories category and 20 products in the Clothing category.
                         - :orange[**Relationship between PSC and PP**]: This graph illustrates the relationship between Standard Product Cost and Product Price or Unit Price. For example, with a production cost of 2.172 per unit and a selling price of 3.578, it shows that the company would profit 1.407 from selling this unit (formula=standard product cost-unit price).
                    ''')

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
                         - :orange[**Data**]: The data used in this visualization is from [Web IMDB](www.imdb.com).
                         - :orange[**First Week Gross Revenue**]: The graph shows the gross revenue of a movies in its first week. It is evident that the movie titled Spider-Man: No Way Home had the highest gross revenue in the first week, amounting to 260.138.569 USD, followed by Jurassic World, which earned 208.806.270 USD in the first week. 
                         - :orange[**Top 5 Movies**]: The graph displays the top 5 movies with the highest gross revenue. It shows that the movie with the highest gross revenue is titled Spider-Man: No Way Home, totaling 814.866.178 USD. Following that is Avatar: The Way of Water with 684.075.767 USD, Jurassic World with 653.406.625 USD, Jurassic World: Fallen Kingdom with 417.719.760 USD, and finally Oppenheimer with 329.862.540 USD.
                         - :orange[**High/Low Budget**]: According to this data, it shows which movie has the highest and lowest budgets. Spider-Man: No Way Home has the highest budget, amounting to 350.000.000.00 USD, while Godzilla has the lowest budget at 175.000.00 USD. The difference in budget between the highest and lowest is 349.825.000.00 USD.
                         - :orange[**Total Movies by Genre**]: This graph shows the total number of films by genre. It can be seen from the graph that the genre most frequently used in films is Action at 29.5% or 36 films, followed by Adventure at 21.3% or 26 films.
                         - :orange[**Total Movies by Year**]: This graph shows the total number of movies per year. It can be seen that from 1997 to 2013, there was only 1 movie each year based on the available data. However, there was an increase to 11 movies in 2024. Perhaps this is due to advancements in technology that have made the movie-making process easier.
                         - :orange[**Top Rating**]: This table shows the ranking of films based on their ratings in order from highest to lowest. The film entitled Dune: Part Two has the highest rating, namely 8.6/10, while the film with the lowest rating is Godzilla: King of the Monsters which only has a rating of 6/10.
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
                              st.write(f"⭐ {row['Rating']:.1f}/10.0")
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
