import pandas as pd
import geopandas as gpd
import folium
from pyproj import Transformer
transformer = Transformer.from_crs("EPSG:5186", "EPSG:4326")
year=20233
df=pd.read_csv('merged_data_20232.csv', encoding='cp949')
plot_target='아파트_평균_시가'
cnt_sum = df.groupby('행정동_코드_명')[plot_target].sum().reset_index()

shp_path = r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_hangjeongdong_geodata\gwangjin_dong.shp"
gdf = gpd.read_file(shp_path, encoding='euc-kr')
merged = gdf.merge(cnt_sum, left_on='ADM_NM', right_on='행정동_코드_명')
m=folium.Map(location=[37.546635, 127.085750], zoom_start=14)
# choropleth 레이어 추가
folium.Choropleth(
    geo_data=merged,
    name='choropleth',
    data=merged,
    columns=['ADM_NM', plot_target],
    key_on='feature.properties.ADM_NM',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    bins=20,
    legend_name=plot_target, reset=True,
    tooltip='{:.2f}'.format

).add_to(m)

# 클릭시 팝업 추가
for idx, row in merged.iterrows():
    popup_text = f"{row['행정동_코드_명']}: {row[plot_target]}"
    latitude, longitude = transformer.transform(row.geometry.centroid.y, row.geometry.centroid.x)
    folium.Marker(
        location=[latitude, longitude],  # 위도, 경도 순서로 전달
        popup=popup_text,
        tooltip=row['행정동_코드_명']
    ).add_to(m)
    print(row['행정동_코드_명'], latitude, longitude)
# 지도 저장
output_html = f'folium_{plot_target}_{year}.html'
m.save(output_html)

print("저장 완료:", output_html)