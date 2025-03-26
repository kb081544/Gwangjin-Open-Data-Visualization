import geopandas as gpd
import pandas as pd
# Pandas 출력 옵션 설정
pd.set_option('display.max_columns', None)  # 모든 열 보이기
pd.set_option('display.max_rows', None)     # 모든 행 보이기

# shapefile 불러오기
shapefile_path = r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_dong_geodata\gwangjin_dong.shp"
#shapefile_seoul=r"C:\Users\user\PycharmProjects\gwangjingu\BND_ADM_DONG_PG\BND_ADM_DONG_PG.shp"
gdf = gpd.read_file(shapefile_path,encodings='euc-kr')
#gdf_seoul=gpd.read_file(shapefile_seoul, encodings='euc-kr')
# 속성 데이터프레임 내용 출력
print(gdf)
#print(gdf_seoul)
