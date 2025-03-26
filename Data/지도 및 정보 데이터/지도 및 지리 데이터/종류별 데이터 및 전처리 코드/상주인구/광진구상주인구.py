import pandas as pd

df1 = pd.read_csv('서울시 상권분석서비스(상주인구-행정동).csv', encoding='cp949')
df2 = pd.read_csv(rf"C:\Users\user\PycharmProjects\gwangjingu\행정동법정동코드\gwangjin_dong.csv", encoding='cp949')
merged_df = pd.merge(df1, df2, left_on='행정동_코드_명', right_on='읍면동명', how='inner')
num_cols = len(merged_df.columns)
last_two_cols = merged_df.columns[num_cols - 2:]
merged_df = merged_df.drop(columns=last_two_cols)
print(merged_df)
for code, group in merged_df.groupby('기준_년분기_코드'):
    filename = f"merged_data_{code}.csv"
    group.to_csv(filename, index=False, encoding='cp949')
    print(f"Saved {filename}")