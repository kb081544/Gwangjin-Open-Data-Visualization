'''
https://golmok.seoul.go.kr/stateArea.do
'''
'''
https://data.seoul.go.kr/dataList/OA-15572/S/1/datasetView.do
'''
import pandas as pd
import geopandas as gpd
import folium
from branca.colormap import linear
from pyproj import Transformer
transformer = Transformer.from_crs("EPSG:5186", "EPSG:4326")

date=2022
df_seoul = pd.read_csv(fr"C:\Users\user\PycharmProjects\gwangjingu\0411\상권분석서비스(점포)\서울시_상권분석서비스(점포-상권)_2022년\서울시_상권분석서비스(점포-상권)_{date}년.csv",dtype=str, encoding="cp949", index_col=False)
df_gwangjin=pd.read_csv(fr"C:\Users\user\PycharmProjects\gwangjingu\0408\Commercial\광진구상권.csv", encoding='utf-8', dtype=str)
gwangjin_commercial_district=df_gwangjin['상권_코드']
gwangjin=df_seoul[df_seoul['상권_코드'].isin((gwangjin_commercial_district))]
print(gwangjin)
gwangjin_seoul_df = gwangjin.merge(df_gwangjin, on='상권_코드', how='left')
gwangjin_seoul_df.loc[:,['점포_수','개업_율','폐업_률']]=gwangjin_seoul_df.loc[:,['점포_수','개업_율','폐업_률']].astype(float)
sales_columns = [col for col in gwangjin_seoul_df.columns if '매출' in col]
grouped_df_sales = gwangjin_seoul_df.groupby('행정동_코드_명')[sales_columns].sum().reset_index()
grouped_df_sales.to_csv(fr'C:\Users\user\PycharmProjects\gwangjingu\행정동분류\상권매출_행정동별합.csv', encoding='cp949')

print(grouped_df_sales)

shp_path = r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_hangjeongdong_geodata\gwangjin_dong.shp"
gdf = gpd.read_file(shp_path, encoding='euc-kr')
merged = gdf.merge(grouped_df_sales, left_on='ADM_NM', right_on='행정동_코드_명')
print(merged)
m=folium.Map(location=[37.546635, 127.085750], zoom_start=14)
# choropleth 레이어 추가
folium.Choropleth(
    geo_data=merged,
    name='choropleth',
    data=merged,
    columns=['ADM_NM', '당월_매출_금액'],
    key_on='feature.properties.ADM_NM',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    bins=20,
    legend_name='월별 매출 금액', reset=True,
    tooltip='매출 금액: ${:.2f}'.format

).add_to(m)

# 클릭시 팝업 추가
for idx, row in merged.iterrows():
    popup_text = f"{row['행정동_코드_명']}: {row['당월_매출_금액']}"
    latitude, longitude = transformer.transform(row.geometry.centroid.y, row.geometry.centroid.x)
    popup_text += f"<br>위도: {latitude:.2f}, 경도: {longitude:.2f}"
    folium.Marker(
        location=[latitude, longitude],  # 위도, 경도 순서로 전달
        popup=popup_text,
        tooltip=row['행정동_코드_명']
    ).add_to(m)

# 지도 저장
output_html = f'gwangjin_dong_sales_folium_{date}.html'
m.save(output_html)

print("저장 완료:", output_html)

# gwangjin_grouped=gwangjin.groupby(['상권_코드','상권_코드_명']).sum().reset_index()
# print(gwangjin_grouped)
# total_sales_amount = gwangjin['당월_매출_금액'].sum()
# total_sales_count = gwangjin['당월_매출_건수'].sum()
#
# # 결과 출력
# print("총 매출 금액:", total_sales_amount)
# print("총 매출 건수:", total_sales_count)
#
# gwangjin_grouped=gwangjin_grouped.drop(gwangjin_grouped.columns[[2,3,4,5,6]], axis=1)
# gwangjin_grouped.to_csv('광진상권분석_2021.csv', encoding='utf-8-sig')