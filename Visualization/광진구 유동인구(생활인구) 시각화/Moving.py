'''
https://data.seoul.go.kr/dataList/OA-14979/F/1/datasetView.do
'''
import pandas as pd
import geopandas as gpd
import folium
from pyproj import Transformer
import re

def remove_je(text):
    # '제'를 제거하고 숫자와 '동'이 함께 나오는 경우 처리
    text = re.sub(r'(?<=\D)제', '', text)  # 숫자 앞의 '제' 제거
    text = re.sub(r'제(?=\d*동)', '', text)  # '제' 뒤의 숫자와 '동' 사이의 '제' 제거
    return text

def replace_je(text):
    # '제'를 제거하고 앞의 글자 두 개가 붙은 경우 처리
    text = re.sub(r'(?<=\D)제', '', text)  # 숫자 앞의 '제' 제거
    return text

transformer = Transformer.from_crs("EPSG:5186", "EPSG:4326")
date=2403
df_population = pd.read_csv(fr"C:\Users\user\PycharmProjects\gwangjingu\0408\유동인구(생활인구)\LOCAL_PEOPLE_DONG_20{date}\LOCAL_PEOPLE_DONG_20{date}.csv",index_col=False,  encoding='utf-8')
df_dong_code = pd.read_csv(r"C:\Users\user\PycharmProjects\gwangjingu\행정동법정동코드\KIKcd_H.20240208.csv", encoding='cp949')

df_dong_code['행정동코드'] = df_dong_code['행정동코드'].astype(str).str[:-2]
df_dong_code['행정동코드'] = df_dong_code['행정동코드'].astype(int)
gwangjin_h = df_dong_code[df_dong_code['시군구명'] == '광진구']
gwangjin_h=gwangjin_h[1:]
print(gwangjin_h)
gwangjin_h_list=gwangjin_h["행정동코드"].tolist()
gwangjin_h_cnt=len(gwangjin_h_list)
print(gwangjin_h_cnt)
# 생활인구 데이터에서 광진구 행정동 코드의 소분류가 아닌 행만 필터링
filtered_local_people_dong = df_population[df_population["행정동코드"].isin(gwangjin_h_list)]
filtered_data = pd.merge(filtered_local_people_dong, gwangjin_h[['행정동코드', '읍면동명']], on='행정동코드', how='left')
filtered_data['읍면동명'] = filtered_data['읍면동명'].apply(remove_je)
print(filtered_data)

time=13 #시간대 변수
day=1 #날짜변수
time_slice = filtered_data[(filtered_data['기준일ID'] == 20240302) & (filtered_data['시간대구분'] == 13)]
print(time_slice.iloc[:, 21:29])
time_slice['20대부터60대여자인구수'] = time_slice.iloc[:, 7:15].sum(axis=1)
time_slice['20대부터60대남자인구수'] = time_slice.iloc[:, 21:29].sum(axis=1)
time_slice['20대부터60대총인구수'] = time_slice['20대부터60대여자인구수'] + time_slice['20대부터60대남자인구수']
#time_slice=filtered_data[time*gwangjin_h_cnt:time*gwangjin_h_cnt+gwangjin_h_cnt]
#print(time_slice)
time_slice.to_csv('생활인구(소비계층20대~50대).csv', encoding='cp949')
shp_path = r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_hangjeongdong_geodata\gwangjin_dong.shp"

gdf = gpd.read_file(shp_path, encoding='euc-kr')

merged = gdf.merge(time_slice, left_on='ADM_NM', right_on='읍면동명')
m=folium.Map(location=[37.546635, 127.085750], zoom_start=14)
folium.Choropleth(
    geo_data=merged,
    name='choropleth',
    data=merged,
    columns=['ADM_NM', '총생활인구수'],
    key_on='feature.properties.ADM_NM',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    bins=20,
    legend_name='생활인구수', reset=True,
).add_to(m)
# 클릭시 팝업 추가
for idx, row in merged.iterrows():
    popup_text = f"{row['읍면동명']}: {row['총생활인구수']}"
    latitude, longitude = transformer.transform(row.geometry.centroid.y, row.geometry.centroid.x)
    popup_text += f"<br>위도: {latitude:.2f}, 경도: {longitude:.2f}"
    folium.Marker(
        location=[latitude, longitude],  # 위도, 경도 순서로 전달
        popup=popup_text,
        tooltip=row['읍면동명']
    ).add_to(m)

output_html = f'gwangjin_dong_de_facto_population_{date}_time_{time}_day{day}.html'
m.save(output_html)

print("저장 완료:", output_html)
time_slice.to_csv(f'유동인구_{date}_time_{time}.csv', encoding='cp949')