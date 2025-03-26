import folium
import requests
import json
import pandas as pd
from folium.plugins import MarkerCluster
#https://teddylee777.github.io/visualization/folium/
#37.546635, 127.085750
m=folium.Map(location=[37.546635, 127.085750], zoom_start=14)
street_lamp_data=pd.read_csv(r"C:\Users\user\PycharmProjects\gwangjingu\0401\서울특별시 광진구_가로등 위치정보_20220214.csv", encoding='cp949')
smart_street_lamp_data=pd.read_csv(r"C:\Users\user\PycharmProjects\gwangjingu\0401\서울특별시_광진구_스마트가로등_20230401.csv", encoding='cp949')
smart_street_lamp_data_ll=smart_street_lamp_data[['위도','경도']]
street_lamp_data_ll=street_lamp_data[['위도','경도']]
gwangjin_geo=r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_geodata\gwangjin_map.json"
print(smart_street_lamp_data_ll.head())

folium.GeoJson(gwangjin_geo, name="GwangJin-Gu").add_to(m)

from folium.plugins import MarkerCluster

marker_cluster = MarkerCluster().add_to(m)
for idx, row in street_lamp_data_ll.iterrows():
    folium.Marker(location=[row['위도'], row['경도']], popup='광진구 가로등', icon=folium.Icon(color='red')).add_to(marker_cluster)
for idx, row in smart_street_lamp_data_ll.iterrows():
    folium.Marker(location=[row['위도'], row['경도']], popup='광진구 스마트 가로등', icon=folium.Icon(color='orange')).add_to(marker_cluster)

#m.show_in_browser()
m.save("map_with_markers_clustering.html")