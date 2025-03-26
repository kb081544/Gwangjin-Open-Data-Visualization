import folium
import pandas as pd
import geopandas as gpd
from folium.plugins import MarkerCluster

# 광진구 경계 데이터 로드
gwangjin_geo = r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_geodata\gwangjin_map.json"

# 가로등 데이터 로드
street_lamp_data = gpd.read_file(r"C:\Users\user\PycharmProjects\gwangjingu\0401\전국 가로등비상벨 지도\FSN_30_20221130_G_001.shp", encoding='utf-8')
print(street_lamp_data.head())
# 광진구 경계 다각형 추출
gwangjin_polygon = gpd.read_file(gwangjin_geo)

# 광진구 경계 내 가로등 데이터 필터링
street_lamp_data_gwangjin = street_lamp_data[street_lamp_data.geometry.within(gwangjin_polygon.unary_union)]
street_lamp_data_gwangjin_ll=street_lamp_data_gwangjin[['LA','LO']]
print(street_lamp_data_gwangjin.head())
# 지도 생성
m = folium.Map(location=[37.546635, 127.085750], zoom_start=14)

# 광진구 경계 GeoJSON을 folium으로 추가
folium.GeoJson(gwangjin_geo, name="GwangJin-Gu").add_to(m)

# 마커 클러스터 생성
#marker_cluster = MarkerCluster().add_to(m)

# 필터링된 가로등 데이터에 대해 마커 생성하여 클러스터에 추가
for idx, row in street_lamp_data_gwangjin_ll.iterrows():
    folium.Marker(location=[row['LO'], row['LA']], popup='광진구 가로등', icon=folium.Icon(color='red')).add_to(m)

# HTML 파일로 저장
m.save("map_with_markers_clustering_street_lamp_without_clustering.html")
m.show_in_browser()
