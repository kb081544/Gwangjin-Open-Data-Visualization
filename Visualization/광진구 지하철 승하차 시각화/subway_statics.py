import csv
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
date=2301
stations=pd.read_csv('gwangjin_subway_stations.txt',dtype=str,delimiter=',', encoding='utf-8')

data = pd.read_csv(fr'CARD_SUBWAY_MONTH_20{date}.csv', delimiter=',', dtype=str, encoding='utf-8',index_col=False)
seoul_stations=pd.read_csv('서울시 역사마스터 정보.csv',dtype=str, encoding='cp949',index_col=False)
filtered_rows = []
gwangjin_stations = seoul_stations[seoul_stations['역사명'].isin(stations)]
gwangjin_stations=gwangjin_stations.sort_values('역사명')
gwangjin_stations=gwangjin_stations.drop_duplicates(subset=['역사명'])
print(gwangjin_stations)

filtered_data = data[data['역명'].str.strip().isin(stations)]
filtered_data.loc[:, '승차총승객수'] = filtered_data['승차총승객수'].astype(int)
filtered_data.loc[:, '하차총승객수'] = filtered_data['하차총승객수'].astype(int)
station_data = filtered_data.groupby('역명').agg({'승차총승객수': 'mean', '하차총승객수': 'mean'})
print(station_data)

gwangjin_map = gpd.read_file(r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_geodata\gwangjin_map.shp")
print("gwangjin_stations 열 이름:", gwangjin_stations.columns)
print("station_data 열 이름:", station_data.columns)
merged_data = gwangjin_stations.merge(station_data, left_on='역사명', right_index=True)
gwangjin_gu=r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_geodata\gwangjin_map.json"
m=folium.Map(location=[37.546635, 127.085750], zoom_start=14)

folium.GeoJson(gwangjin_gu, name="GwangJin-Gu").add_to(m)

# 역 위치와 승하차총승객수 표시
marker_cluster=MarkerCluster().add_to(m
                                      )
# for idx, row in merged_data.iterrows():
#     # 마커 아이콘에 숫자와 마커 아이콘을 함께 표시
#     icon_html = f"<div style='font-size: 20pt;'>{row['승차총승객수']:.0f}<br><div>{row['하차총승객수']:.0f}"
#     folium.Marker(location=[row['위도'], row['경도']],
#                   popup=f"역명: {row['역사명']}",
#                   icon=folium.DivIcon(html=icon_html,
#                                       icon_size=(30, 30))).add_to(marker_cluster)

for dx, row in merged_data.iterrows():
    iframe = folium.IFrame(row['역사명'])
    popup = folium.Popup(iframe, min_width=140, max_width=150)
    icon_html = f"<div style='font-size: 20pt;'>{row['승차총승객수']:.0f}<br><div>{row['하차총승객수']:.0f}"
    folium.CircleMarker(
        location=[row['위도'], row['경도']],
        radius=row['승차총승객수']/300,  # 원의 크기를 승차총승객수에 따라 조절
        color='blue',
        fill_color='blue', popup=popup
    ).add_to(m)
# HTML 파일로 저장
m.save(fr'gwangjin_subway_stations_{date}.html')
