import streamlit as st
from pathlib import Path
import base64
import matplotlib.pyplot as plt
import pandas as pd
from gtts import gTTS
from deep_translator import GoogleTranslator
import io

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

     data = ["Database Dump_AW", "Scrapping IMDB"]
     data_dipilih = st.sidebar.selectbox("__Pilih data__", data)

     st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
     st.sidebar.markdown('''<small>[FP_Davis_2024](https://github.com/IlhamBerlianO/FP_Davis_2024)  | 2024 | [Ilham Berlian O](https://github.com/IlhamBerlianO/)</small>''', unsafe_allow_html=True)
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
          st.title("Scrapping IMDB")
          # Deskripsi
          st.write(f'Visualisasi data film dengan menggunakan data dari www.imdb.com')
        
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
        
          st.subheader("Film Ratings")
          fig, ax = plt.subplots()
          sns.barplot(data=baca, x='Rating', y='Title', ax=ax, palette="viridis")
          st.pyplot(fig)

          # Pie chart untuk distribusi genre
          st.subheader("Genre Distribution")
          genre_counts = baca['Genre'].str.split(', ').explode().value_counts()
          fig, ax = plt.subplots()
          ax.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("viridis", len(genre_counts)))
          ax.axis('equal')
          st.pyplot(fig)
          
          # Line chart untuk pendapatan kotor berdasarkan tanggal rilis
          st.subheader("Gross Revenue Over Time")
          baca['Opening_week_date'] = pd.to_datetime(baca['Opening_week_date'])
          sorted_data = baca.sort_values(by='Opening_week_date')
          fig, ax = plt.subplots()
          sns.lineplot(data=sorted_data, x='Opening_week_date', y='Gross_us', ax=ax, marker='o')
          ax.set_title('Gross Revenue Over Time')
          ax.set_xlabel('Release Date')
          ax.set_ylabel('Gross Revenue (US)')
          st.pyplot(fig)
        
          # Judul aplikasi
          st.markdown("<h1 class='centered'>Top Picks</h1>", unsafe_allow_html=True)
        
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
