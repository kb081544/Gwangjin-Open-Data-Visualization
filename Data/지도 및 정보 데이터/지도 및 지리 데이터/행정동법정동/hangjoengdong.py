import pandas as pd

# CSV 파일을 읽어옵니다.
df = pd.read_csv('KIKcd_H.20240208.csv', encoding='cp949')

# 시군구명이 '광진구'인 행만 선택합니다.
df_gwangjin = df[df['시군구명'] == '광진구']

# 읍면동명에서 '제'를 제외한 이름을 추출합니다.
df_gwangjin['읍면동명'] = df_gwangjin['읍면동명'].str.replace('제', '', regex=False)
df_gwangjin = df_gwangjin.dropna(subset=['읍면동명'])

# 행정동명과 행정동코드 열만 선택하여 새로운 데이터프레임을 만듭니다.
new_df = df_gwangjin[['행정동코드', '읍면동명']]

# 새로운 CSV 파일로 저장합니다.
new_df.to_csv('gwangjin_dong.csv', index=False, encoding='cp949')

# 결과를 확인합니다.
print(new_df)
