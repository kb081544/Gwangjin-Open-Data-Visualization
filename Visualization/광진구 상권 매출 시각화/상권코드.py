#11215
import pandas as pd

# CSV 파일 읽기
df = pd.read_csv(r"C:\Users\user\PycharmProjects\gwangjingu\0408\commercialDistrict.csv", dtype=str, index_col=False, encoding='cp949')

# '자치구_코드_명' 열이 '광진구' 인 행들만 선택
gwangjin_df = df[df['자치구_코드_명'] == '광진구']

# 결과 출력
print(gwangjin_df)
gwangjin_df.to_csv('광진구상권.csv', encoding="utf-8-sig")
