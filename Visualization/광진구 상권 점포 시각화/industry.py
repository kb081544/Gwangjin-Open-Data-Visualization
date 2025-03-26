import pandas as pd

# CSV 파일을 읽어옵니다.
df = pd.read_csv('광진구사업체분포.csv', encoding='utf-8', header=False)

# '숙박 및 음식점업'이라는 열 이름이 포함된 열을 찾습니다.
columns_with_industry = [col for col in df.columns if '숙박 및 음식점업' in col]

# 두 번째로 나오는 열을 선택합니다.
target_column = columns_with_industry[1]

# 해당 열과 세 번째 열을 합쳐서 새로운 열을 생성합니다.
new_column = df['동별(3)'] + '_' + df[target_column]

# 새로운 열을 데이터프레임에 추가합니다.
df['동별(3)_숙박음식점'] = new_column

# 필요한 열만 선택하여 새로운 데이터프레임을 만듭니다.
new_df = df[['동별(1)', '동별(2)', '동별(3)_숙박음식점']]

# 결과를 출력합니다.
print(new_df)
