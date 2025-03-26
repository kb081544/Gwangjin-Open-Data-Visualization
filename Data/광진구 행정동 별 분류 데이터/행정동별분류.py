import os
import pandas as pd

# 작업할 디렉토리 경로
directory = r'C:\Users\user\PycharmProjects\gwangjingu\행정동분류'

# 빈 리스트 생성 - 모든 파일을 담을 리스트
all_dfs = []

# 디렉토리 내의 모든 CSV 파일을 반복하여 처리
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # 파일 경로
        file_path = os.path.join(directory, filename)
        # CSV 파일을 DataFrame으로 읽기
        df = pd.read_csv(file_path, encoding='cp949')

        # '행정동_코드_명'을 기준으로 열을 정렬하고 해당 열 이전 열은 삭제
        sorted_columns = sorted(df.columns, key=lambda x: x != '행정동_코드_명')
        df_sorted = df.reindex(columns=sorted_columns)

        # '행정동_코드_명' 이전의 열 삭제
        index_of_code = sorted_columns.index('행정동_코드_명')
        columns_to_drop = sorted_columns[:index_of_code]
        df_sorted.drop(columns=columns_to_drop, inplace=True)

        # '행정동_코드_명'을 기준으로 열을 정렬한 DataFrame을 리스트에 추가
        all_dfs.append(df_sorted)

# 첫 번째 데이터프레임을 기준으로 나머지 데이터프레임을 차례대로 병합
merged_df = all_dfs[0]
for df in all_dfs[1:]:
    merged_df = pd.merge(merged_df, df, on='행정동_코드_명', how='outer')

# 결과를 확인할 수 있도록 출력
print(merged_df)
merged_df = merged_df.loc[:, ~merged_df.columns.str.contains('^Unnamed')]
merged_df.to_csv('행정동별_feature.csv', encoding='cp949')