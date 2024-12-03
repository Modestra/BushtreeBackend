#!/usr/bin/env python
# coding: utf-8

# In[2]:

#Импорт библиотек
import pandas as pd
import numpy as np
import warnings, csv

from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
pd.options.mode.chained_assignment = None 
from bushtree.models import *
from django.conf import settings
warnings.filterwarnings("ignore")


class FlowersSet():
    """Базовый класс для цветников. Используется для генерации цветников и подходящих для него цветов"""

    columns_name = ['id', 'frost_resistance_zone','decorative_terms_start',
            'decorative_terms_end', 'height_from',
            'height_to', 'color_main', 'color_other']
    def __init__(self):
        pass
    pass


    def dataset_creategarden(color_main, color_other):
       
        # Обработка запроса с сайта
        input_request = pd.DataFrame({'height_from': [50],
                                      'height_to': [200],
                                      'color_main': [color_main],
                                      'color_other': [color_other]})
        
        columns_name = ['id', 'frost_resistance_zone','decorative_terms_start',
            'decorative_terms_end', 'height_from',
            'height_to', 'color_main', 'color_other']
        
        columns_name_dataset = ['flower_beds', 'decorative_terms_start', 'decorative_terms_end', 
                                'height_from', 'height_to', 'color_main', 'color_other', 'cloud_number']
        
        if settings.DB_CSV:
            with (f'{settings.BASE_DIR}/bushtree/flowers.csv') as csvfile:
                writer = csv.writer(csvfile, quotechar=",", quoting=csv.QUOTE_MINIMAL)
                writer.writerow()
        else:
            # Подключение к датасетам
            main_data = pd.read_csv(f'{settings.BASE_DIR}/bushtree/flowers.csv')
            df = pd.read_csv(f'{settings.BASE_DIR}/bushtree/Update.csv')
       
        # Датасет с цветами
        columns_name = ['id', 'frost_resistance_zone','decorative_terms_start',
                   'decorative_terms_end', 'height_from',
                   'height_to', 'color_main', 'color_other']
        
        data_flowers = df[columns_name]
        data_flowers = data_flowers[data_flowers['frost_resistance_zone'] < 5].drop('frost_resistance_zone', axis=1).reset_index(drop=True)

        # Датасет цветников
        flower_beds = main_data.pivot_table(index=['flower_beds'],
                                            values=['height_from', 'height_to'],
                                            aggfunc={'height_from': "min", 'height_to': "max"}).reset_index()

        for i in flower_beds['flower_beds'].unique():
            flower_beds.loc[(flower_beds['flower_beds'] == i), 'color_main'] = main_data[main_data['flower_beds']==i]['color_main'].value_counts().index[0]
            if i != 32:
                flower_beds.loc[(flower_beds['flower_beds'] == i), 'color_other'] = main_data[main_data['flower_beds']==i]['color_main'].value_counts().index[1]
            else:
                flower_beds.loc[(flower_beds['flower_beds'] == i), 'color_other'] = main_data[main_data['flower_beds']==i]['color_main'].value_counts().index[0]


        # Рекомендация цветника
        
        # Кодирование цветов в датасете с цветниками
        x = pd.DataFrame(set(flower_beds['color_main'].to_list() + flower_beds['color_other'].to_list()))
        encoder = OrdinalEncoder()
        encoder.fit(x)
        
        flower_beds_coded = flower_beds.drop(['flower_beds'], axis=1)
        flower_beds_coded['color_main'] = pd.DataFrame(encoder.transform(flower_beds[['color_main']]))
        flower_beds_coded['color_other'] = pd.DataFrame(encoder.transform(flower_beds[['color_other']]))


        # Нормирование числовых данных
        scaler = StandardScaler()
        scaler.fit(flower_beds_coded[['height_from','height_to']])
              
        flower_beds_coded[flower_beds_coded.drop(['color_main', 'color_other'], axis=1).columns.to_list()] = scaler.transform(flower_beds_coded.drop(['color_main', 'color_other'], axis=1))

        # Обучение рекомендации цветника
        neigh = KNeighborsClassifier(n_neighbors=3)
        neigh.fit(flower_beds_coded, flower_beds['flower_beds'])
        
        # Обработка пользовательского запроса
        input_request['color_main'] = pd.DataFrame(encoder.transform(input_request[['color_main']]))
        input_request['color_other'] = pd.DataFrame(encoder.transform(input_request[['color_other']]))
        input_request[input_request.drop(['color_main',	'color_other'], axis=1).columns.to_list()] = scaler.transform(input_request.drop(['color_main',	'color_other'], axis=1))
     
        flower_beds_num = []
        for i in flower_beds.iloc[neigh.predict_proba(input_request).argsort(axis=1)[:,:-4:-1][0]]['flower_beds']:
            flower_beds_num.append(i)
        flower_beds_num.sort(key=None, reverse=False)
               
        return flower_beds_num

    def GetFlowers(flower_beds_num : list):
        """Возвращает имена цветов, подходящие для этого цветника."""
        flowers_list = []

        columns_name = ['id', 'frost_resistance_zone','decorative_terms_start',
            'decorative_terms_end', 'height_from',
            'height_to', 'color_main', 'color_other']
        columns_flower_name = ['flower_beds', 
            'decorative_terms_start', 'decorative_terms_end', 'height_from', 
            'height_to', 'color_main', 'color_other', 'cloud_number']
        
        if settings.DB_CSV:
            with open("base_flowerdataset.csv", newline=",") as csvfile:
                writer = csv.writer(f'{settings.BASE_DIR}/bushtree/base_flowerdataset.csv', quotechar=',', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(columns_name)
                
        else:
            # Подключение к датасетам
            main_data = pd.read_csv(f'{settings.BASE_DIR}/bushtree/flowers.csv')
            df = pd.read_csv(f'{settings.BASE_DIR}/bushtree/Update.csv')
        
        data_flowers = df[columns_name]
        data_flowers = data_flowers[data_flowers['frost_resistance_zone'] < 5].drop('frost_resistance_zone', axis=1).reset_index(drop=True)
        
        #Пользователь выбирает из 3 вариантов и генерирует подходящие цветы для этих вариантов
        flowers_from_main_data = main_data[['flower_beds', 'decorative_terms_start', 'decorative_terms_end', 'height_from', 'height_to', 'color_main', 'color_other', 'cloud_number']]
        flowers_from_main_data_coded = flowers_from_main_data.drop(['cloud_number'], axis=1)
        
        for i in flower_beds_num:
            for j in range(len(flowers_from_main_data[flowers_from_main_data['flower_beds'] == int(i)])):
                color_main = flowers_from_main_data[flowers_from_main_data['flower_beds'] == int(i)]['color_main'].values[j]
                color_other = flowers_from_main_data[flowers_from_main_data['flower_beds'] == int(i)]['color_other'].values[j] # Получение основного и второстепенного цвета цветка
                temp_data = data_flowers[(data_flowers.color_main == color_main) & (data_flowers.color_other == color_other)] #формирование временной таблицы цветов из бд отфильтрованная по цвету
                temp_scaler = StandardScaler() # Обязательно не пустой!
                temp_scaler.fit(temp_data[['decorative_terms_start', 'decorative_terms_end', 'height_to']])
                temp_data.loc[:, ['decorative_terms_start', 'decorative_terms_end', 'height_to']] = temp_scaler.transform(temp_data[['decorative_terms_start', 'decorative_terms_end', 'height_to']]) # Стандартизирование числовых данных
                
                if len(temp_data) < 3:
                    neigh_temp = KNeighborsClassifier(n_neighbors=1, weights='distance')
                    neigh_temp.fit(temp_data[['decorative_terms_start', 'decorative_terms_end', 'height_to']], temp_data['id']) #Обучение рекомендации цветка
                else:
                    neigh_temp = KNeighborsClassifier(n_neighbors=3, weights='distance')
                    neigh_temp.fit(temp_data[['decorative_terms_start', 'decorative_terms_end', 'height_to']], temp_data['id']) #Обучение рекомендации цветка

                flower = flowers_from_main_data_coded[flowers_from_main_data_coded['flower_beds'] == int(i)][['decorative_terms_start', 'decorative_terms_end', 'height_to']].iloc[j:j+1]
                flower.loc[:, ['decorative_terms_start', 'decorative_terms_end', 'height_to']] = temp_scaler.transform(flower[['decorative_terms_start', 'decorative_terms_end', 'height_to']])

                for k in temp_data.iloc[neigh_temp.predict_proba(flower).argsort(axis=1)[:,:-2:-1][0]]['id']:
                    flowers_list.append(df[df['id'] == k]['name'].values[0])      
            break
        return flowers_list