# -*- coding: utf-8 -*-
#paketler
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import seaborn as sns
import folium
import geopandas as gpd
import plotly.express as px
from PIL import Image
import numpy as np

st.set_page_config(layout="wide",initial_sidebar_state='collapsed')

#Veri seti içeri aktarma ve manipülasyon
history = pd.read_csv('C:/Users/monster/Desktop/Gıda_app/history.csv')
future = pd.read_csv('C:/Users/monster/Desktop/Gıda_app/future.csv')
tum = pd.read_csv('C:/Users/monster/Desktop/Gıda_app/tum.csv')
ilceler = gpd.read_file('https://raw.githubusercontent.com/tahasarnic/ilceler/master/turkiye-ilceler.geojson')
tum['Bölge'] = tum['Bölge'].astype('object')


#Başlık
row0_0, row0_1 = st.beta_columns([0.9, 0.1])
with row0_0:
    st.markdown('# Ankara Ovalarında İklim Değişikliğine Dirençli Tarım')
    st.markdown('Aşağıdaki grafikte X ve Y eksenlerini sıcaklık, yağış ve diğer hava durumu faaliyetlerine göre belirleyip, parametreler arasındaki ilişkileri inceleyebilirsiniz.')
    st.markdown('**Not:** Baloncuk büyüklükleri seçime göre arpa veya buğday verimleriyle orantılı olarak büyüyüp küçülmektedir.')
with row0_1:
    st.image("https://www.freeiconspng.com/thumbs/agriculture-icon-png/agriculture-icon-image-gallery-16.png")

st.markdown('## Agro-Ekolojik Bölge Analizi')

#Gapminder-Tarla-Filtreler
row1_0, row1_0_0, row1_1, row1_2, row1_3, row1_4= st.beta_columns(6)
with row1_0:
    arpa_bugday = st.radio('Ürün seçiniz:', ['Arpa Verim', 'Buğday Verim'])
with row1_0_0:
    eksen_x = st.selectbox('X-ekseni seçiniz:', ['Sıcaklık', 'Yağış', 'Diğer'])
    eksen_y = st.selectbox('Y-ekseni seçiniz:', ['Sıcaklık', 'Yağış', 'Diğer'])
with row1_1:
    ay = st.selectbox('Ay seçiniz:', [1,2,3,4,5,6,7,8,9,10,11,12])
with row1_2:
    sicaklik = st.selectbox('Sıcaklık parametresi seçiniz:', ['Ort. Günlük Sıcaklık Farkı', 'GOrtSıcOrt', 'GMinSıcOrt', 'GMinSıcMin', 'GMinSıcMax', 'GMaxSıcOrt', 'GMaxSıcMin', 'MaxGMaxSıc'])
    with st.beta_expander("Sıcaklık parametre kısaltmalarının açıklamaları için tıklayınız"):
        image = Image.open('C:/Users/monster/Desktop/Gıda_app/sıcaklık.PNG')
        st.image(image)
with row1_3:
    yagis = st.selectbox('Yağış parametresi seçiniz:', ['Yoğun Yağış Sayısı', 'Aşırı Yağış Sayısı', 'Toplam Yağış (mm)', 'Yağışlı Gün Sayısı'])
with row1_4:
    diger = st.selectbox('Diğer parametrelerden seçiniz:', ['Biyolojik Gün Sayısı', 'Don Gün Sayısı', 'Buzlu Gün Sayısı', 'Yaz Günleri Sayısı', 'Tropik Geceler Sayısı'])

row2_0, row2_1 = st.beta_columns([1,1])
with row2_0:
    fig = px.scatter(tum, x = [sicaklik if eksen_x == 'Sıcaklık' else yagis if eksen_x == 'Yağış' else diger][0]+str(ay), y = [sicaklik if eksen_y == 'Sıcaklık' else yagis if eksen_y == 'Yağış' else diger][0]+str(ay), animation_frame='yil', size = arpa_bugday, color = 'Bölge',
          color_discrete_map={1:'#e64545',
                               2:'#5c95c2',
                               3:'#4daf4a',
                               4:'#984ea3'},
          animation_group='İlçe',
          hover_name = 'İlçe',
          range_y = [tum[[sicaklik if eksen_y == 'Sıcaklık' else yagis if eksen_y == 'Yağış' else diger][0]+str(ay)].min(),tum[[sicaklik if eksen_y == 'Sıcaklık' else yagis if eksen_y == 'Yağış' else diger][0]+str(ay)].max()],
          range_x = [tum[[sicaklik if eksen_x == 'Sıcaklık' else yagis if eksen_x == 'Yağış' else diger][0]+str(ay)].min(),tum[[sicaklik if eksen_x == 'Sıcaklık' else yagis if eksen_x == 'Yağış' else diger][0]+str(ay)].max()],
          template = 'none',
          size_max=17
          )
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 700
    st.plotly_chart(fig)

with row2_1:
    alt_bolge = pd.DataFrame({'İlçe':list(history['İlçe'].unique()) + ['Yenimahalle', 'Etimesgut', 'Altındağ', 'Mamak', 'Çankaya', 'Keçiören', 'Sincan']})
    alt_bolge['Bölge'] = [3, 1, 1, 1, 3, 2, 2, 2, 4, 1, 4, 4, 4, 4, 4, 5,5,5,5,5,5,5]
    alt_bolge_harita = alt_bolge.merge(ilceler, how = 'left', left_on = 'İlçe', right_on = 'name')
    alt_bolge_harita = gpd.GeoDataFrame(alt_bolge_harita)
    m = folium.Map(location = [39.92077, 32.85411], zoom_start=7, width=700,height=400)

    #Renk Tonlu Harita
    choropleth = folium.Choropleth(
        geo_data=alt_bolge_harita,
        data = alt_bolge,
        columns = ['İlçe', 'Bölge'],
        key_on = 'feature.properties.İlçe',
        fill_color='Set1',
        line_opacity = 0.2,
        fill_opacity = 0.8,
        legend_name='Verim',
        bins = [1,2,3,4,5,6],
        highlight = True
        ).add_to(m)

    folium.LayerControl().add_to(m)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['İlçe', 'Bölge'], labels=True)
        )

    with st.beta_expander("Agro-ekolojik alt bölge bilgileri için tıklayınız"):
        image = Image.open('C:/Users/monster/Desktop/Gıda_app/altbolgeler.PNG')
        st.image(image)
    folium_static(m)

#########################################################################################################
zamansal = pd.read_csv('C:/Users/monster/Desktop/Gıda_app/zaman.csv').drop('Unnamed: 0', axis = 1)
st.markdown('## Zamansal Hava Faaliyetleri Değişimi ve Ürün Bazında Verim Analizi')
row3_0, row3_1 = st.beta_columns([1,3])

with row3_0:
    ilce = st.multiselect('İlçe(ler) seçiniz:', list(zamansal['İlçe'].unique()),  default=['Ayaş', 'Çubuk'])
    parametre_zaman = st.selectbox('Parametre seçiniz:', ['Ort. Günlük Sıcaklık Farkı', 'GOrtSıcOrt', 'GMinSıcOrt', 'GMinSıcMin', 'GMinSıcMax', 'GMaxSıcOrt', 'GMaxSıcMin', 'MaxGMaxSıc',
                                                         'Yoğun Yağış Sayısı', 'Aşırı Yağış Sayısı', 'Toplam Yağış (mm)', 'Yağışlı Gün Sayısı',
                                                         'Biyolojik Gün Sayısı', 'Don Gün Sayısı', 'Buzlu Gün Sayısı', 'Yaz Günleri Sayısı', 'Tropik Geceler Sayısı'])
    with st.beta_expander("Sıcaklık parametre kısaltmalarının açıklamaları için tıklayınız"):
        image = Image.open('C:/Users/monster/Desktop/Gıda_app/sıcaklık.PNG')
        st.image(image)
    
with row3_1:
    zamansal['Zaman'] = 'Geçmiş'
    zamansal.loc[zamansal['yil'] > 2019, 'Zaman'] = 'Gelecek'
    fig = px.line(zamansal[(zamansal['İlçe'].isin(ilce)) & (zamansal['vars'] == parametre_zaman)].sort_values(by = ['yil', 'nums']), x = 'tarih', y = 'value', color = 'İlçe', template = 'none', width = 1000, height = 500, title = str(parametre_zaman)+' '+ 'Parametresinin Zamana Bağlı Değişimi')
    fig.add_vrect(x0="2020-1", x1="2040-12", 
              annotation_text="Gelecek Tahminleri", annotation_position="top left",
              fillcolor="green", opacity=0.15, line_width=0, annotation=dict(font_size=16))
    fig.update_xaxes(title = dict(text = 'Tarih'))
    fig.update_yaxes(title = dict(text = parametre_zaman))
    st.plotly_chart(fig)
#####################################################################################################
row4_0, row4_1 = st.beta_columns([1,3])
heat = pd.read_csv('C:/Users/monster/Desktop/Gıda_app/tum.csv').iloc[:,2:]
with row4_0:
    urun = st.radio('Ürün seçiniz', ['Arpa Verim', 'Buğday Verim'])
    ilce_heat = st.multiselect('İlçe(ler) seçiniz', list(heat['İlçe'].unique()),  default=['Ayaş', 'Çubuk', 'Güdül', 'Gölbaşı(Ankara)'])
    baslangic = st.number_input('Başlangıç yılı giriniz:', value = 2020)
    bitis = st.number_input('Bitiş yılı giriniz:', value = 2040)
    
with row4_1:
    fig = px.imshow(heat[(heat['yil'] >= baslangic) & (heat['yil'] <=  bitis) & (heat['İlçe'].isin(ilce_heat))].pivot_table(index = 'İlçe', columns = 'yil', values = urun), color_continuous_scale = px.colors.sequential.OrRd,
               labels=dict(x="Yıl", y="İlçe", color=urun),
               width = 1000,
               title = 'Zaman Bazlı Verim Analizi')
    fig.update_layout(
    title={
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    st.plotly_chart(fig)

###################################################################################################
st.markdown('## Buğday ve Arpanın Gelecek Serüveni')
st.markdown('Aşağıdaki haritada belirtilen ürün verim öngörüleri yapay öğrenme modellerinden elde edilmiştir. İlgili ürün veriminin tahmininde kullanılan **önemli tahmin edici parametreler**, kullanılan yapay öğrenme algoritmalarıyla bulunmuştur. Bu parametrelere ilişkin yıllık değişim tablosu, "Ürün Verim Öngörüleri" haritalandırma çalışması altındadır.')
gelecek = pd.read_csv('C:/Users/monster/Desktop/Gıda_app/tum.csv')
ilceler = gpd.read_file('https://raw.githubusercontent.com/tahasarnic/ilceler/master/turkiye-ilceler.geojson')
gelecek = tum.iloc[:,2:]
gelecek = gelecek[gelecek['yil'] > 2019].reset_index(drop = True)
gelecek_geo = gelecek.merge(ilceler, how = 'left', left_on = 'İlçe', right_on = 'name')
gelecek_geo = gpd.GeoDataFrame(gelecek_geo)
    

row5_0, row5_1 = st.beta_columns([0.3, 0.7])

with row5_0:
    yil_map = st.select_slider('Yıl seçiniz:', options=list(gelecek.yil.unique()))
    urun_map = st.radio('Ürün:', ['Arpa Verim', 'Buğday Verim'])
    
with row5_1:
    m = folium.Map(location = [39.92077, 32.85411], zoom_start=7, width = '%100', height = '%80')
    #Renk Tonlu Harita
    choropleth = folium.Choropleth(
        geo_data=gelecek_geo[gelecek_geo['yil'] == yil_map],
        data = gelecek[gelecek['yil'] == yil_map],
        columns = ['İlçe', urun_map],
        key_on = 'feature.properties.İlçe',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=urun_map + ' ' + 'Tahmini'
        ).add_to(m)

    folium.LayerControl().add_to(m)
    choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['İlçe',urun_map], labels=True)
        )        
    st.markdown('### Ürün Verim Öngörüleri')
    folium_static(m)     


############################################################################################################
tablo = pd.read_csv('C:/Users/monster/Desktop/Gıda_app/tum.csv')
tablo = tablo[tablo['yil'] > 2019].iloc[:,2:]
arpa_onemli = pd.read_excel('C:/Users/monster/Desktop/Gıda_app/arpa_onemli.xls')
bugday_onemli = pd.read_excel('C:/Users/monster/Desktop/Gıda_app/bugday_onemli.xls')
arpa_parametre = dict()
for i in range(len(arpa_onemli)):
    arpa_parametre[arpa_onemli['ilce'][i]] = list((arpa_onemli['Parametre1'][i], arpa_onemli['Parametre2'][i], arpa_onemli['Parametre3'][i]))
bugday_parametre = dict()
for i in range(len(bugday_onemli)):
    bugday_parametre[bugday_onemli['ilce'][i]] = list((bugday_onemli['Parametre1'][i], bugday_onemli['Parametre2'][i], bugday_onemli['Parametre3'][i]))

row6_0, row6_1 = st.beta_columns([0.3, 0.7])

with row6_0:
    urun_tablo = st.radio('Önemli parametre değerlerini görmek istediğiniz ürünü seçiniz:', ['Arpa Verim', 'Buğday Verim'])
    ilce_tablo = st.selectbox('Önemli parametre değerlerini görmek istediğiniz ilçeyi seçiniz:', list(tablo['İlçe'].unique()))
    with st.beta_expander("Sıcaklık parametre kısaltmalarının açıklamaları için tıklayınız"):
        image = Image.open('C:/Users/monster/Desktop/Gıda_app/sıcaklık.PNG')
        st.image(image)
with row6_1:
    if urun_tablo == 'Arpa Verim':
        st.table(tablo[tablo['İlçe'] == ilce_tablo][['yil'] + arpa_parametre[ilce_tablo]].reset_index(drop = True).style.bar(subset=arpa_parametre[ilce_tablo], align='mid', color=['#FF8C7E', '#BDEFB8']).hide_index())
    else:
        st.table(tablo[tablo['İlçe'] == ilce_tablo][['yil'] + bugday_parametre[ilce_tablo]].reset_index(drop = True).style.bar(subset=bugday_parametre[ilce_tablo], align='mid', color=['#FF8C7E', '#BDEFB8']).hide_index())
    