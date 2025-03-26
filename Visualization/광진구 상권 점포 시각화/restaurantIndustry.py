'''
https://data.seoul.go.kr/dataList/OA-15578/S/1/datasetView.do
'''
import csv
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from pyproj import Transformer
from folium.plugins import MarkerCluster
transformer = Transformer.from_crs("EPSG:5186", "EPSG:4326")
year=2022
industry=pd.read_csv(r"C:\Users\user\PycharmProjects\gwangjingu\0408\광진구상권.csv",dtype=str,delimiter=',', encoding='utf-8')
commercialAnalysis=pd.read_csv(fr"C:\Users\user\PycharmProjects\gwangjingu\0408\외식업\서울시_상권분석서비스(점포-상권)_{year}년\서울시_상권분석서비스(점포-상권)_{year}년.csv", encoding='cp949', dtype=object, index_col=None)
# 'industry' 데이터프레임에서 광진구 상권의 상권 코드를 가져옵니다.
gwangjin_code = industry[industry['자치구_코드_명'] == '광진구']['상권_코드'].unique()

# 'commercialAnalysis' 데이터프레임에서 '상권_코드'가 광진구 상권코드에 속하는 행을 필터링합니다.
filtered_analysis = commercialAnalysis[commercialAnalysis['상권_코드'].isin(gwangjin_code)]

# 'industry' 데이터프레임에서 '상권_코드'에 해당하는 '행정동_코드_명'을 가져옵니다.
gwangjin_hangjeongdong = industry[industry['상권_코드'].isin(gwangjin_code)][['상권_코드', '행정동_코드_명']]

# 'commercialAnalysis'와 'industry' 데이터프레임을 상권 코드를 기준으로 병합합니다.
merged_data = pd.merge(filtered_analysis, gwangjin_hangjeongdong, on='상권_코드')
merged_data = merged_data.astype({'기준_년분기_코드': int, '상권_코드': int, '점포_수': int, '유사_업종_점포_수': int, '개업_율': int, '개업_점포_수': int, '폐업_률': int, '폐업_점포_수': int, '프랜차이즈_점포_수': int})

'''
'기준_년분기_코드', '상권_구분_코드_명', '상권_코드', '상권_코드_명', '서비스_업종_코드',
'서비스_업종_코드_명', '점포_수', '유사_업종_점포_수', '개업_율', '개업_점포_수', '폐업_률',
'폐업_점포_수', '프랜차이즈_점포_수', '행정동_코드_명'
'''

plot_target_service='한식음식점'
cnt_service=merged_data[merged_data['서비스_업종_코드_명']==plot_target_service]
plot_target='점포_수'
cnt_sum = merged_data.groupby('행정동_코드_명')[plot_target].sum().reset_index()

dong_column = pd.DataFrame(columns=['행정동_코드_명'])

# 업종 리스트ㅂ
restaurant_list = ['한식음식점', '중식음식점', '일식음식점', '제과점']

# 각 업종별로 데이터프레임 생성 후 병합
for r in restaurant_list:
    cnt_restaurant_sum = merged_data[merged_data['서비스_업종_코드_명'] == r].groupby('행정동_코드_명')['점포_수'].sum().reset_index()
    cnt_restaurant_sum.rename(columns={'점포_수': f'{r}_점포_수'}, inplace=True)  # 열 이름 변경
    dong_column = pd.merge(dong_column, cnt_restaurant_sum, on='행정동_코드_명', how='outer')

print(dong_column)
dong_column.to_cst
'''
plot_target='폐업_률'
cnt_sum = merged_data.groupby('행정동_코드_명')[plot_target].sum().reset_index()
'''

print(cnt_sum)


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
    popup_text += f"<br>위도: {latitude:.2f}, 경도: {longitude:.2f}"
    folium.Marker(
        location=[latitude, longitude],  # 위도, 경도 순서로 전달
        popup=popup_text,
        tooltip=row['행정동_코드_명']
    ).add_to(m)

# 지도 저장
output_html = f'gwangjin_dong_sales_folium__{plot_target}_{year}.html'
m.save(output_html)

print("저장 완료:", output_html)
