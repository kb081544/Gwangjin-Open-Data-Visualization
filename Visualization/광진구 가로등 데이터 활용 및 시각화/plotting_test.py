import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

#https://wonhwa.tistory.com/22
plt.rcParams["font.family"]='NanumGothic'
plt.rcParams["figure.figsize"]=(10,10)
file=r"C:\Users\user\PycharmProjects\gwangjingu\gwangjin_geodata\gwangjin_map.shp"
pll=gpd.read_file(file, encodings='cp949')

street_lamp_data=pd.read_csv(r"C:\Users\user\PycharmProjects\gwangjingu\0401\서울특별시 광진구_가로등 위치정보_20220214.csv")
smart_street_lamp_data=pd.read_csv(r"C:\Users\user\PycharmProjects\gwangjingu\0401\서울특별시_광진구_스마트가로등_20230401.csv")
pll.plot()
plt.show()