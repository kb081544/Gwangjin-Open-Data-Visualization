'''
https://www.blcm.go.kr/stat/customizedStatic/CustomizedStaticSupplyList.do?pageIndex=20
'''
import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from pyproj import Transformer
transformer = Transformer.from_crs("EPSG:5186", "EPSG:4326")
# https://www.bdsplanet.com/map/realprice_map.ytp?ubt_mode=explore_basic
import pandas as pd
# 내 API Key
# LAPJM831-LAPJ-LAPJ-LAPJ-LAPJM831HH
# CSV 파일 읽기
df = pd.read_csv('2022.11 기준 서울시 25개 자치구의 노후건축물 현황(30년 이상) 및 노후건축물 중 조적구조 통계현황.csv',encoding='cp949',index_col=False,thousands=',')

# Gwangjin-Gu만 필터링
df_gwangjin = df[df['시군구'] == '광진구']
df_gwangjin.loc[:, ['대지면적(㎡)']] = df_gwangjin[['대지면적(㎡)']].astype(float)

# 행정동으로 정렬
df_sorted = df_gwangjin.sort_values(by='법정동')
visitor_counts_by_dong = df_gwangjin.groupby('법정동')['대지면적(㎡)'].sum()
visitor_counts_by_dong.name='대지면적(㎡)'
print(visitor_counts_by_dong)
shp_path = r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_beopjeongdong_geodata\gwangjin_dong.shp"
gdf = gpd.read_file(shp_path, encoding='euc-kr')
gdf.crs="epsg:5174" #5178
merged = gdf.merge(visitor_counts_by_dong, left_on='EMD_KOR_NM', right_on='법정동')
print(merged)
from mpl_toolkits.axes_grid1 import make_axes_locatable
fig,ax=plt.subplots(figsize=(15,15),facecolor='white')
merged.boundary.plot(ax=ax, color='white')
merged.plot(column='대지면적(㎡)', cmap='coolwarm', ax=ax, alpha=4)
plt.show()
plt.savefig('30yearsold_ratio.png')