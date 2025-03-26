import csv
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point
import re
# https://data.seoul.go.kr/dataList/OA-12912/S/1/datasetView.do#
def remove_numbers(station_name):
    return re.sub(r'\(\d+\)', '', station_name)
date=2402
bus_data = pd.read_csv(f'BUS_STATION_BOARDING_MONTH_20{date}.csv', delimiter=',', dtype=str, encoding='cp949',index_col=False)
seoul_bus_stops =pd.read_csv('서울시 버스정류소 위치정보.csv',dtype=str, encoding='cp949',index_col=False)
gwangjin_map = gpd.read_file(r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_geodata\gwangjin_map.shp")

# X좌표와 Y좌표를 활용하여 GeoDataFrame으로 변환
geometry = [Point(xy) for xy in zip(seoul_bus_stops['X좌표'], seoul_bus_stops['Y좌표'])]
seoul_bus_stops_gdf = gpd.GeoDataFrame(seoul_bus_stops, crs=gwangjin_map.crs, geometry=geometry)

# 서울시 버스정류소 데이터 중에서 광진구에 해당하는 정류소를 추출
gwangjin_bus_stops = gpd.sjoin(seoul_bus_stops_gdf, gwangjin_map, op='within')
bus_data['역명'] = bus_data['역명'].apply(remove_numbers)
gwangjin_bus_data=bus_data['버스정류장ARS번호'].isin(gwangjin_bus_stops['정류소번호'])
# 결과를 출력
print(gwangjin_bus_stops)
filtered_bus_data = bus_data[gwangjin_bus_data]
print(filtered_bus_data)
#여기까지 성공
gwangjin_bus_stops['정류소명'] = gwangjin_bus_stops['정류소명'].apply(remove_numbers)

filtered_bus_data.loc[:, '승차총승객수'] = filtered_bus_data['승차총승객수'].astype(int)
filtered_bus_data.loc[:, '하차총승객수'] = filtered_bus_data['하차총승객수'].astype(int)
# 역별로 하루 평균 승차총승객수와 하차총승객수 계산
gwangjin_avg_boarding = filtered_bus_data.groupby('버스정류장ARS번호')['승차총승객수'].mean().reset_index()
gwangjin_avg_alighting = filtered_bus_data.groupby('버스정류장ARS번호')['하차총승객수'].mean().reset_index()

# 두 데이터프레임을 합치기
gwangjin_avg_passengers = pd.merge(gwangjin_avg_boarding, gwangjin_avg_alighting, on='버스정류장ARS번호', suffixes=('_승차', '_하차' ))
#gwangjin_avg_passengers = pd.merge(gwangjin_avg_passengers, gwangjin_bus_stops, how='inner', on='정류소번호')
merged_df = pd.merge(gwangjin_avg_passengers, gwangjin_bus_stops, left_on='버스정류장ARS번호', right_on='정류소번호')
print(merged_df)
# 결과 확인
print(gwangjin_avg_passengers)
print(filtered_bus_data)
gwangjin_avg_passengers.to_csv('gwangjin_avg_passengers.csv', encoding='cp949')
# Folium을 사용하여 지도에 시각화
m=folium.Map(location=[37.546635, 127.085750], zoom_start=14)
from folium.plugins import MarkerCluster

for i in range(len(merged_df)):
    iframe = folium.IFrame(merged_df.iloc[i]['정류소명'])
    popup = folium.Popup(iframe, min_width=140, max_width=150)
    folium.CircleMarker(

        location=[merged_df.iloc[i]['Y좌표'], merged_df.iloc[i]['X좌표']],
        radius=merged_df.iloc[i]['승차총승객수']/10,  # 원의 크기를 승차총승객수에 따라 조절
        color='blue',
        fill_color='blue', popup=popup
    ).add_to(m)

# 결과 지도를 HTML 파일로 저장하거나 직접 렌더링
m.save(f'passenger_map_{date}.html')