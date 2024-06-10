import streamlit as st
from pathlib import Path
import base64
import matplotlib.pyplot as plt
import pandas as pd
from gtts import gTTS
from deep_translator import GoogleTranslator
import io
import seaborn as sns
import altair as alt
import os
import mysql.connector
from mysql.connector import Error
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data

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
     st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=32 height=32>](https://streamlit.io/)'''.format(img_to_bytes("gambar/logomark_website.png")), unsafe_allow_html=True)
     st.sidebar.header('Dashboard')

     data_dipilih = st.sidebar.selectbox("__Pilih data__", ["Database Dump_AW", "Scrapping IMDB"])

     # Logika untuk mengubah sidebar berdasarkan pilihan dropdown
     if data_dipilih == "Database Dump_AW":
          st.sidebar.subheader("Sidebar berubah untuk Database Dump_AW")
          filter_scrapping = st.sidebar.selectbox("Genres", ["Filter A", "Filter B", "Filter C"])
     elif data_dipilih == "Scrapping IMDB":
          st.sidebar.subheader("Filter:")
          filter_scrapping = st.sidebar.selectbox("Genres", ["Filter A", "Filter B", "Filter C"])
          filter_scrapping_2 = st.sidebar.selectbox("Color", ["Filter D", "Filter E", "Filter F"])
          filtro3 = st.sidebar.slider("Rating", 0.0, 10.0)

     st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
     st.sidebar.markdown('''<small>[FP_Davis_2024](https://github.com/IlhamBerlianO/FP_Davis_2024)  | 21082010034 | [Ilham Berlian O](https://github.com/IlhamBerlianO/)</small>''', unsafe_allow_html=True)
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
                         st.write("Connection to database was successful")
                         return connection
               except Error as e:
                    print(f"Error: '{e}'")
                    return None
          
          connection = create_connection()

          col1, col2, col3 = st.columns(3)
     
          #######################################
          # COLUMN 1
          #######################################
          # Display text
          col1.subheader('Display text')
          col1.code('''
               st.text('Fixed width text')
               st.markdown('_Markdown_') # see #*
               st.caption('Balloons. Hundreds of them...')
               st.latex(r\'\'\' e^{i\pi} + 1 = 0 \'\'\')
               st.write('Most objects') # df, err, func, keras!
               st.write(['st', 'is <', 3]) # see *
               st.title('My title')
               st.header('My header')
               st.subheader('My sub')
               st.code('for i in range(8): foo()')
          
               # * optional kwarg unsafe_allow_html = True
          ''')
     
          # Display data
          col1.subheader('Display data')
          col1.code('''
               st.dataframe(my_dataframe)
               st.table(data.iloc[0:10])
               st.json({'foo':'bar','fu':'ba'})
               st.metric(label="Temp", value="273 K", delta="1.2 K")
          ''')
          
          # Display media
          col1.subheader('Display media')
          col1.code('''
               st.image('./header.png')
               st.audio(data)
               st.video(data)
          ''')
     
          # Columns
          col1.subheader('Columns')
          col1.code('''
               col1, col2 = st.columns(2)
               col1.write('Column 1')
               col2.write('Column 2')
          
               # Three columns with different widths
               col1, col2, col3 = st.columns([3,1,1])
               # col1 is wider
                        
               # Using 'with' notation:
               >>> with col1:
               >>>     st.write('This is column 1')
                        
          ''')
     
          # Tabs
          col1.subheader('Tabs')
          col1.code('''
               # Insert containers separated into tabs:
               >>> tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
               >>> tab1.write("this is tab 1")
               >>> tab2.write("this is tab 2")
          
               # You can also use "with" notation:
               >>> with tab1:
               >>>   st.radio('Select one:', [1, 2])
          ''')
     
          # Control flow
          col1.subheader('Control flow')
          col1.code('''
               # Stop execution immediately:
               st.stop()
               # Rerun script immediately:
               st.experimental_rerun()
          
               # Group multiple widgets:
               >>> with st.form(key='my_form'):
               >>>   username = st.text_input('Username')
               >>>   password = st.text_input('Password')
               >>>   st.form_submit_button('Login')
          ''')
         
          # Personalize apps for users
          col1.subheader('Personalize apps for users')
          col1.code('''
               # Show different content based on the user's email address.
               >>> if st.user.email == 'jane@email.com':
               >>>    display_jane_content()
               >>> elif st.user.email == 'adam@foocorp.io':
               >>>    display_adam_content()
               >>> else:
               >>>    st.write("Please contact us to get access!")
          ''')
     
          #######################################
          # COLUMN 2
          #######################################
          # Display interactive widgets
          col2.subheader('Display interactive widgets')
          col2.code('''
               st.button('Hit me')
               st.data_editor('Edit data', data)
               st.checkbox('Check me out')
               st.radio('Pick one:', ['nose','ear'])
               st.selectbox('Select', [1,2,3])
               st.multiselect('Multiselect', [1,2,3])
               st.slider('Slide me', min_value=0, max_value=10)
               st.select_slider('Slide to select', options=[1,'2'])
               st.text_input('Enter some text')
               st.number_input('Enter a number')
               st.text_area('Area for textual entry')
               st.date_input('Date input')
               st.time_input('Time entry')
               st.file_uploader('File uploader')
               st.download_button('On the dl', data)
               st.camera_input("一二三,茄子!")
               st.color_picker('Pick a color')
          ''')
     
          col2.code('''
               # Use widgets\' returned values in variables
               >>> for i in range(int(st.number_input('Num:'))): foo()
               >>> if st.sidebar.selectbox('I:',['f']) == 'f': b()
               >>> my_slider_val = st.slider('Quinn Mallory', 1, 88)
               >>> st.write(slider_val)
          ''')
          col2.code('''
               # Disable widgets to remove interactivity:
               >>> st.slider('Pick a number', 0, 100, disabled=True)
          ''')
     
          # Build chat-based apps
          col2.subheader('Build chat-based apps')
          col2.code('''
               # Insert a chat message container.
               >>> with st.chat_message("user"):
               >>>    st.write("Hello 👋")
               >>>    st.line_chart(np.random.randn(30, 3))
          
               # Display a chat input widget.
               >>> st.chat_input("Say something")          
          ''')
     
          col2.markdown('<small>Learn how to [build chat-based apps](https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps)</small>', unsafe_allow_html=True)
     
          # Mutate data
          col2.subheader('Mutate data')
          col2.code('''
               # Add rows to a dataframe after
               # showing it.
               >>> element = st.dataframe(df1)
               >>> element.add_rows(df2)
          
               # Add rows to a chart after
               # showing it.
               >>> element = st.line_chart(df1)
               >>> element.add_rows(df2)
          ''')
     
          # Display code
          col2.subheader('Display code')
          col2.code('''
               st.echo()
               >>> with st.echo():
               >>>     st.write('Code will be executed and printed')
          ''')
     
          # Placeholders, help, and options
          col2.subheader('Placeholders, help, and options')
          col2.code('''
               # Replace any single element.
               >>> element = st.empty()
               >>> element.line_chart(...)
               >>> element.text_input(...)  # Replaces previous.
          
               # Insert out of order.
               >>> elements = st.container()
               >>> elements.line_chart(...)
               >>> st.write("Hello")
               >>> elements.text_input(...)  # Appears above "Hello".
          
               st.help(pandas.DataFrame)
               st.get_option(key)
               st.set_option(key, value)
               st.set_page_config(layout='wide')
               st.experimental_show(objects)
               st.experimental_get_query_params()
               st.experimental_set_query_params(**params)
          ''')
     
          #######################################
          # COLUMN 3
          #######################################
          # Connect to data sources
          col3.subheader('Connect to data sources')
          col3.code('''
               st.experimental_connection('pets_db', type='sql')
               conn = st.experimental_connection('sql')
               conn = st.experimental_connection('snowpark')
          
               >>> class MyConnection(ExperimentalBaseConnection[myconn.MyConnection]):
               >>>    def _connect(self, **kwargs) -> MyConnection:
               >>>        return myconn.connect(**self._secrets, **kwargs)
               >>>    def query(self, query):
               >>>       return self._instance.query(query)
          ''')
     
     
          # Optimize performance
          col3.subheader('Optimize performance')
          col3.write('Cache data objects')
          col3.code('''
               # E.g. Dataframe computation, storing downloaded data, etc.
               >>> @st.cache_data
               ... def foo(bar):
               ...   # Do something expensive and return data
               ...   return data
               # Executes foo
               >>> d1 = foo(ref1)
               # Does not execute foo
               # Returns cached item by value, d1 == d2
               >>> d2 = foo(ref1)
               # Different arg, so function foo executes
               >>> d3 = foo(ref2)
               # Clear all cached entries for this function
               >>> foo.clear()
               # Clear values from *all* in-memory or on-disk cached functions
               >>> st.cache_data.clear()
          ''')
          col3.write('Cache global resources')
          col3.code('''
               # E.g. TensorFlow session, database connection, etc.
               >>> @st.cache_resource
               ... def foo(bar):
               ...   # Create and return a non-data object
               ...   return session
               # Executes foo
               >>> s1 = foo(ref1)
               # Does not execute foo
               # Returns cached item by reference, s1 == s2
               >>> s2 = foo(ref1)
               # Different arg, so function foo executes
               >>> s3 = foo(ref2)
               # Clear all cached entries for this function
               >>> foo.clear()
               # Clear all global resources from cache
               >>> st.cache_resource.clear()
          ''')
          col3.write('Deprecated caching')
          col3.code('''
               >>> @st.cache
               ... def foo(bar):
               ...   # Do something expensive in here...
               ...   return data
               >>> # Executes foo
               >>> d1 = foo(ref1)
               >>> # Does not execute foo
               >>> # Returns cached item by reference, d1 == d2
               >>> d2 = foo(ref1)
               >>> # Different arg, so function foo executes
               >>> d3 = foo(ref2)
          ''')
     
          # Display progress and status
          col3.subheader('Display progress and status')
          col3.code('''
               # Show a spinner during a process
               >>> with st.spinner(text='In progress'):
               >>>   time.sleep(3)
               >>>   st.success('Done')
               
               # Show and update progress bar
               >>> bar = st.progress(50)
               >>> time.sleep(3)
               >>> bar.progress(100)
               
               st.balloons()
               st.snow()
               st.toast('Mr Stay-Puft')
               st.error('Error message')
               st.warning('Warning message')
               st.info('Info message')
               st.success('Success message')
               st.exception(e)
          ''')
         
     elif data_dipilih == "Scrapping IMDB":
          # Judul aplikasi
          st.markdown("""
               <h1 style='text-align: center;'>Scrapping IMDB</h1>
          """, unsafe_allow_html=True)
          st.markdown('''<hr>''', unsafe_allow_html=True)

          # Deskripsikan col
          col1, col2, col3 = st.columns([.9, 1.8, 1])

          # Membaca file excel
          baca = pd.read_excel("scrapping_imdb/top_picks_data.xlsx")
          # Ambil data film
          title = baca['Title'].tolist()
          gross = baca['Gross_us'].tolist()
          summary = baca['Summary'].tolist()
          image = baca['Image'].tolist()
          rating = baca['Rating'].tolist()
          genre = baca['Genre'].tolist()
          runtime = baca['Runtime'].tolist()
          # Ganti nilai "-" dengan tanggal default (misal: 1 Januari 1900)
          default_date = pd.to_datetime('1900-01-01')
          baca['Opening_week_date'] = baca['Opening_week_date'].replace('-', default_date)
          # Ambil tahun dari kolom Opening_week_date
          baca['Year'] = pd.to_datetime(baca['Opening_week_date'], errors='coerce').dt.year
          # Hilangkan baris dengan nilai yang tidak valid
          baca = baca.dropna(subset=['Year'])
          # Hitung jumlah film berdasarkan tahun
          jumlah_film_per_tahun = baca['Year'].value_counts().sort_index()

          # Menampilkan konten 
          with col1:
               sorted_data = baca.sort_values(by='Budget', ascending=False)
               top_film = sorted_data.iloc[0]
               low_film = sorted_data.iloc[-1]

               budget_delta = top_film['Budget'] - low_film['Budget']

               st.subheader("Top/Low Budget")

               st.metric(label=f"{top_film['Title']}", value=f"${top_film['Budget']:,.2f}", delta=f"${budget_delta:,.2f}")
               st.metric(label=f"{low_film['Title']}", value=f"${low_film['Budget']:,.2f}", delta=f"-${budget_delta:,.2f}")
               
               with st.expander('About', expanded=True):
                    st.write('''
                         - Data: [Web IMDB](www.imdb.com).
                         - :orange[**Top/Low Budget**]: Movies that have the highest and lowest budgets.
                         - :orange[**Top 5 Movies**]: 5 highest grossing movies.
                         - :orange[**Top Rating**]: The order of movies is based on ratings in order from highest to lowest.
                    ''')

          with col2:
               st.subheader("Top 5 Movies")
               
               top5_grossing_films = baca.nlargest(5, 'Gross_us').sort_values(by='Gross_us', ascending=False)
               
               chart = alt.Chart(top5_grossing_films).mark_bar().encode(
                    x='Gross_us:Q',
                    y=alt.Y('Title:N', sort='-x'),
                    tooltip=['Title', 'Gross_us']
               ).configure_axis(
                    grid=False
               ).interactive()

               st.altair_chart(chart, use_container_width=True)

               st.subheader("Number of Films Released per Year")

               chartOptions = {
                    "layout": {
                         "textColor": 'white',
                         "background": {
                              "type": 'solid',
                              "color": 'rgb(14, 17, 23)'
                         }
                    },
                    "grid": {
                         "vertLines": {
                              "color": 'rgba(42, 46, 57, 0.1)',
                              "visible": 'false'
                         },
                         "horzLines": {
                              "color": 'rgba(42, 46, 57, 0.1)', 
                              "visible": 'false'
                         }
                    }
               }

               # Tampilkan grafik area berdasarkan jumlah film per tahun
               renderLightweightCharts([
               {
                    "chart": chartOptions,
                    "series": [{
                         "type": 'Area',
                         "data": jumlah_film_per_tahun.tolist(),
                         "options": {}
                    }],
               }
               ], 'area')

          with col3:
               st.subheader('Top Rating')
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
          
          st.markdown('''<hr>''', unsafe_allow_html=True)
        
          # Judul aplikasi
          st.markdown("<h1 class='centered'>Movie List</h1>", unsafe_allow_html=True)
        
          # Folder gambar
          image_folder = "gambar"

          cols = st.columns(6)
          num_cols = 6

          for i in range(len(title)):
               with cols[i % num_cols]:
                    image_path = os.path.join(image_folder, image[i])
                    if os.path.exists(image_path):
                         st.image(image_path, use_column_width=True)
                    else:
                         st.markdown("![Image not available](https://via.placeholder.com/150)")
                    st.markdown(title[i])
                    st.markdown(rating[i])
                    st.button("Detail", key=f"button_{i}")
                    
          # Menambahkan elemen kosong jika jumlah film tidak mengisi seluruh kolom pada baris terakhir
          if len(title) % num_cols != 0:
               for _ in range(num_cols - len(title) % num_cols):
                    st.empty()

          # Pilih saham dari dropdown
          selected_stock = st.selectbox('Pilih Film:', title)
        
          # Temukan indeks saham yang dipilih di daftar perusahaan
          index = title.index(selected_stock)
        
          # Tampilkan detail perusahaan yang dipilih
          st.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid'>](https://streamlit.io/)'''.format(img_to_bytes(f"gambar/{image[index]}")), unsafe_allow_html=True)
          st.write(f'Judul Film: {title[index]}')
          st.write(f'Rating: {rating[index]}/10')
          st.write(f'Genre: {genre[index]}')
          st.write(f'Waktu: {runtime[index]} Menit')
          st.write(f'Penjelasan Singkat:')
        
          # Inisialisasi objek Translator
          translator = GoogleTranslator(source='en', target='id')
        
          # Tambahkan tombol untuk membaca deskripsi perusahaan
          if st.button("Translate ke Indonesia"):
               # Translate deskripsi dari bahasa Inggris ke bahasa Indonesia
               summary_id = translator.translate(summary[index])
               summary[index] = summary_id
        
          st.write(summary[index])
        
          # Fungsi untuk merubah teks deskripsi menjadi suara
          def text_to_speech(text):
               tts = gTTS(text=text, lang='en')  # Menggunakan gTTS untuk mengonversi teks ke suara dalam bahasa Inggris
               speech = io.BytesIO()
               tts.write_to_fp(speech)
               return speech.getvalue()
        
          # Tambahkan tombol untuk membaca deskripsi perusahaan
          if st.button("Baca Deskripsi"):
               speech_bytes = text_to_speech(summary[index])
               st.audio(speech_bytes, format='audio/mp3')
     else:
          st.write("Data yang dipilih tidak tersedia")

     return None

# Run main()
if __name__ == '__main__':
     main()
