import streamlit as st
from pathlib import Path
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

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
    
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
        # Judul aplikasi
        st.title("Scrapping IMDB")
        st.write("Ini adalah contoh konten yang akan ditampilkan jika Database Dump_AW dipilih.")
        
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
        
        # # Plot grafik
        plt.figure(figsize=(10, 6))
        plt.barh(title, gross, color='#398bff')
        plt.xlabel('Pendapatan ($)')
        plt.ylabel('Judul Film')
        plt.title('Grafik Film Top Picks')
        plt.gca().invert_yaxis() 
        st.pyplot(plt)
        
        # Judul aplikasi
        st.title('Nama Film')
        
        # Pilih saham dari dropdown
        selected_stock = st.selectbox('Pilih Film:', title)
        
        # Temukan indeks saham yang dipilih di daftar perusahaan
        index = title.index(selected_stock)
        
        # Tampilkan detail perusahaan yang dipilih
        st.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid'>](https://streamlit.io/)'''.format(img_to_bytes(f"gambar/{image[index]}")), unsafe_allow_html=True)
        st.write(f'Judul Film: {title[index]}')
        st.write(f'Rating: ${rating[index]}')
        st.write(f'Genre: ${genre[index]}')
        st.write(f'Waktu: ${runtime[index]} Menit')
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
        
        st.write(f'Created by Ilham Berlian Oktavio')

    else:
        st.write("Data yang dipilih tidak tersedia")
        

    return None
    
##########################
# Run main()
##########################
if __name__ == '__main__':
    main()
