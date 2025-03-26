import os
import glob
import numpy as np
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
stations = np.loadtxt(os.path.join(current_dir, 'gwangjin_subway_stations.txt'), dtype=str, delimiter=',',
                      encoding='utf-8')

total_boarding = pd.Series()
total_alighting = pd.Series()
num_files = 0

csv_files = glob.glob(os.path.join(current_dir, 'CARD_SUBWAY_MONTH_*.csv'))

for csv_file in csv_files:
    data = pd.read_csv(csv_file, delimiter=',', dtype=str, encoding='utf-8', index_col=False)
    filtered_data = data[data['역명'].str.strip().isin(stations)]
    filtered_data.loc[:, '승차총승객수'] = filtered_data['승차총승객수'].astype(int)
    filtered_data.loc[:, '하차총승객수'] = filtered_data['하차총승객수'].astype(int)
    station_data = filtered_data.groupby('역명').agg({'승차총승객수': 'mean', '하차총승객수': 'mean'})
    total_boarding = total_boarding.add(station_data['승차총승객수'], fill_value=0)
    total_alighting = total_alighting.add(station_data['하차총승객수'], fill_value=0)
    num_files += 1

average_boarding = total_boarding / num_files
average_alighting = total_alighting / num_files

print("각 역의 모든 CSV 파일의 평균 승차총승객수:")
print(average_boarding)
print("\n각 역의 모든 CSV 파일의 평균 하차총승객수:")
print(average_alighting)
