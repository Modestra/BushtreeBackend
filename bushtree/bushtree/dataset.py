from json import encoder
import pandas as pd
import numpy as np
import psycopg2 as ps
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from django.conf import settings

main_data = pd.read_csv(f"{settings.BASE_DIR}/flowers - Лист1.csv")
df = pd.read_csv(f'{settings.BASE_DIR}/Update_датасет.csv')
def dataset_creategarden():
    data_flowers = df[['id', 'frost_resistance_zone','decorative_terms_start', 'decorative_terms_end', 'height_from', 'height_to', 'color_main', 'color_other']]
    data_flowers = data_flowers[data_flowers['frost_resistance_zone'] < 5]
    data_flowers.loc[data_flowers['decorative_terms_start'] == 'Март', 'decorative_terms_start'] = 3
    data_flowers.loc[data_flowers['decorative_terms_start'] == 'Апрель', 'decorative_terms_start'] = 4
    data_flowers.loc[data_flowers['decorative_terms_start'] == 'Май', 'decorative_terms_start'] = 5
    data_flowers.loc[data_flowers['decorative_terms_start'] == 'Июнь', 'decorative_terms_start'] = 6
    data_flowers.loc[data_flowers['decorative_terms_start'] == 'Июль', 'decorative_terms_start'] = 7
    data_flowers.loc[data_flowers['decorative_terms_start'] == 'Август', 'decorative_terms_start'] = 8
    data_flowers.loc[data_flowers['decorative_terms_start'] == 'Сентябрь', 'decorative_terms_start'] = 9
    data_flowers.loc[data_flowers['decorative_terms_start'] == 'Октябрь', 'decorative_terms_start'] = 10
    data_flowers.loc[data_flowers['decorative_terms_end'] == 'Апрель', 'decorative_terms_end'] = 4
    data_flowers.loc[data_flowers['decorative_terms_end'] == 'Май', 'decorative_terms_end'] = 5
    data_flowers.loc[data_flowers['decorative_terms_end'] == 'Июнь', 'decorative_terms_end'] = 6
    data_flowers.loc[data_flowers['decorative_terms_end'] == 'Июль', 'decorative_terms_end'] = 7
    data_flowers.loc[data_flowers['decorative_terms_end'] == 'Август', 'decorative_terms_end'] = 8
    data_flowers.loc[data_flowers['decorative_terms_end'] == 'Сентябрь', 'decorative_terms_end'] = 9
    data_flowers.loc[data_flowers['decorative_terms_end'] == 'Октябрь', 'decorative_terms_end'] = 10
    data_flowers.loc[data_flowers['decorative_terms_end'] == 'Ноябрь', 'decorative_terms_end'] = 11
    data_flowers.loc[data_flowers['color_other'].isna(), 'color_other'] = 'зеленый'
    data_flowers = data_flowers.drop('frost_resistance_zone', axis=1).reset_index(drop=True)

    flower_beds = main_data.pivot_table(index=['flower_beds'], values=['height_from', 'height_to'], aggfunc={'height_from': "min", 'height_to': "max"}).reset_index()

    for i in flower_beds['flower_beds'].unique():
        flower_beds.loc[(flower_beds['flower_beds'] == i), 'color_main'] = main_data[main_data['flower_beds']==i]['color_main'].value_counts().index[0]
    if i != 32:
        flower_beds.loc[(flower_beds['flower_beds'] == i), 'color_other'] = main_data[main_data['flower_beds']==i]['color_main'].value_counts().index[1]
    else:
        flower_beds.loc[(flower_beds['flower_beds'] == i), 'color_other'] = main_data[main_data['flower_beds']==i]['color_main'].value_counts().index[0]
    
    x = pd.DataFrame(set(flower_beds['color_main'].to_list() + flower_beds['color_other'].to_list()))

    flower_beds_coded = flower_beds.drop(['flower_beds'], axis=1)
    #flower_beds_coded['color_main'] = pd.DataFrame(encoder.transform(flower_beds[['color_main']]))
    #flower_beds_coded['color_other'] = pd.DataFrame(encoder.transform(flower_beds[['color_other']]))
    scaler = StandardScaler()
    scaler.fit(flower_beds_coded[['height_from','height_to']])
    flower_beds_coded[flower_beds_coded.drop(['color_main',	'color_other'], axis=1).columns.to_list()] = scaler.transform(flower_beds_coded.drop(['color_main',	'color_other'], axis=1))
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(flower_beds_coded, flower_beds['flower_beds'])
    request = {'height_from': [25], 'height_to': [150], 'color_main': ['розовый'], 'color_other': ['белый']}
    input_request = pd.DataFrame(request)
    input_request['color_main'] = pd.DataFrame(encoder.transform(input_request[['color_main']]))
    input_request['color_other'] = pd.DataFrame(encoder.transform(input_request[['color_other']]))
    input_request[input_request.drop(['color_main',	'color_other'], axis=1).columns.to_list()] = scaler.transform(input_request.drop(['color_main',	'color_other'], axis=1))

    flower_beds_num = []
    for i in flower_beds.iloc[neigh.predict_proba(input_request).argsort(axis=1)[:,:-4:-1][0]]['flower_beds']:
        flower_beds_num.append(i)
    flower_beds_num.sort(key=None, reverse=False)

    recomended_data = flower_beds.query('flower_beds in @flower_beds_num')
    recomended_data.to_json('file.json', orient = 'split', compression = 'infer')
    json_data = pd.read_json('file.json', orient ='split', compression = 'infer')
    return json_data