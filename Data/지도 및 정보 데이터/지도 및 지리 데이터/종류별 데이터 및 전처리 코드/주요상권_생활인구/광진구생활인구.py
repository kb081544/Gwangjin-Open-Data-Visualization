import pandas as pd

df=pd.read_csv('ES1001AH00101MM2310_csv.csv', encoding='utf-8')
df=df[df['SIGNGU_NM']=='광진구']
print(df)