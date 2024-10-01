
#Импорт библиотек
import pandas as pd
import numpy as np

from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
pd.options.mode.chained_assignment = None 
from django.conf import settings
import json


# # Имитация пользовательского запроса

def dataset_creategarden():
    # In[2]:
    #settings.configure()
    near_flowers = []

    request = {'height_from': [25], 'height_to': [150], 'color_main': ['розовый'], 'color_other': ['белый']}
    input_request = pd.DataFrame(request)


    # # Обработка датасетов

    # In[13]:


    main_data = pd.read_csv(f"{settings.BASE_DIR}/bushtree/flowers.csv")
    df = pd.read_csv(f'{settings.BASE_DIR}/bushtree/Update.csv')


    # In[ ]:


    main_data.watering.unique()


    # In[ ]:


    df.watering.unique()


    # In[ ]:


    df.light.unique()


    # Датасет с цветами

    # In[14]:


    def create_flowers_data():
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
        data_flowers.loc[data_flowers['decorative_terms_end'] == 'Ноябрь', 'decorative_terms_end'] = 10
        data_flowers.loc[data_flowers['color_other'].isna(), 'color_other'] = 'зеленый'
        data_flowers = data_flowers.drop('frost_resistance_zone', axis=1).reset_index(drop=True)
        return data_flowers


    # In[15]:


    data_flowers = create_flowers_data()


    # In[16]:


    data_flowers.head()


    # Датасет цветников

    # In[17]:


    flower_beds = main_data.pivot_table(index=['flower_beds'], values=['height_from', 'height_to'], aggfunc={'height_from': "min", 'height_to': "max"}).reset_index()


    # In[22]:


    for i in flower_beds['flower_beds'].unique():
        flower_beds.loc[(flower_beds['flower_beds'] == i), 'color_main'] = main_data[main_data['flower_beds']==i]['color_main'].value_counts().index[0]
        if i != 32:
            flower_beds.loc[(flower_beds['flower_beds'] == i), 'color_other'] =        main_data[main_data['flower_beds']==i]['color_main'].value_counts().index[1]
        else:
            flower_beds.loc[(flower_beds['flower_beds'] == i), 'color_other'] = main_data[main_data['flower_beds']==i]['color_main'].value_counts().index[0]


    # In[23]:


    flower_beds.head()


    # # Рекомендация цветника

    # ## Кодирование цветов в датасете с цветниками

    # In[24]:


    x = pd.DataFrame(set(flower_beds['color_main'].to_list() + flower_beds['color_other'].to_list()))


    # In[25]:


    encoder = OrdinalEncoder()
    encoder.fit(x)


    # In[26]:


    flower_beds_coded = flower_beds.drop(['flower_beds'], axis=1)


    # In[27]:


    flower_beds_coded['color_main'] = pd.DataFrame(encoder.transform(flower_beds[['color_main']]))
    flower_beds_coded['color_other'] = pd.DataFrame(encoder.transform(flower_beds[['color_other']]))


    # In[28]:


    flower_beds_coded.head()


    # ## Нормирование числовых данных

    # In[29]:


    scaler = StandardScaler()
    scaler.fit(flower_beds_coded[['height_from','height_to']])


    # In[30]:


    flower_beds_coded[flower_beds_coded.drop(['color_main',	'color_other'], axis=1).columns.to_list()] = scaler.transform(flower_beds_coded.drop(['color_main',	'color_other'], axis=1))


    # In[31]:


    flower_beds_coded.head()


    # ## Обучение рекомендации цветника

    # In[32]:


    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(flower_beds_coded, flower_beds['flower_beds'])


    # ## Обработка пользовательского запроса

    # In[33]:


    input_request['color_main'] = pd.DataFrame(encoder.transform(input_request[['color_main']]))
    input_request['color_other'] = pd.DataFrame(encoder.transform(input_request[['color_other']]))
    input_request[input_request.drop(['color_main',	'color_other'], axis=1).columns.to_list()] = scaler.transform(input_request.drop(['color_main',	'color_other'], axis=1))
    input_request


    # In[34]:


    flower_beds_num = []
    for i in flower_beds.iloc[neigh.predict_proba(input_request).argsort(axis=1)[:,:-4:-1][0]]['flower_beds']:
        flower_beds_num.append(i)
        #print('Наиболее близкий цветник', i)
    flower_beds_num.sort(key=None, reverse=False)


    # In[35]:


    recomended_data = flower_beds.query('flower_beds in @flower_beds_num')
    recomended_data


    # In[36]:


    request


    # # Рекомендация цветов

    # In[37]:


    #Таблица с цветами из цветников
    flowers_from_main_data = main_data[['flower_beds', 'decorative_terms_start', 'decorative_terms_end', 'height_from', 'height_to', 'color_main', 'color_other', 'cloud_number']]


    # In[38]:


    flowers_from_main_data.head()


    # In[39]:


    flowers_from_main_data_coded = flowers_from_main_data.drop(['cloud_number'], axis=1)


    # In[47]:


    try:
        for i in flower_beds_num:
            #print(f'Для цветника № {i}:')
            for j in range(len(flowers_from_main_data[flowers_from_main_data['flower_beds'] == i])):
                #print(f'Для облака {j+1} наиболее близкие цветы:')
                color_main = flowers_from_main_data[flowers_from_main_data['flower_beds'] == i]['color_main'].values[j]
                color_other = flowers_from_main_data[flowers_from_main_data['flower_beds'] == i]['color_other'].values[j] # Получение основного и второстепенного цвета цветка
                temp_data = data_flowers[(data_flowers.color_main == color_main) & (data_flowers.color_other == color_other)] #формирование временной таблицы цветов из бд отфильтрованная по цвету
                temp_scaler = StandardScaler()
                temp_scaler.fit(temp_data[['decorative_terms_start', 'decorative_terms_end', 'height_to']])
                temp_data.loc[:, ['decorative_terms_start', 'decorative_terms_end', 'height_to']] = temp_scaler.transform(temp_data[['decorative_terms_start', 'decorative_terms_end', 'height_to']]) # Стандартизирование числовых данных
                
                if len(temp_data) < 3:
                    neigh_temp = KNeighborsClassifier(n_neighbors=1, weights='distance')
                    neigh_temp.fit(temp_data[['decorative_terms_start', 'decorative_terms_end', 'height_to']], temp_data['id']) #Обучение рекомендации цветка
                else:
                    neigh_temp = KNeighborsClassifier(n_neighbors=3, weights='distance')
                    neigh_temp.fit(temp_data[['decorative_terms_start', 'decorative_terms_end', 'height_to']], temp_data['id']) #Обучение рекомендации цветка

                flower = flowers_from_main_data_coded[flowers_from_main_data_coded['flower_beds'] == i][['decorative_terms_start', 'decorative_terms_end', 'height_to']].iloc[j:j+1]
                flower.loc[:, ['decorative_terms_start', 'decorative_terms_end', 'height_to']] = temp_scaler.transform(flower[['decorative_terms_start', 'decorative_terms_end', 'height_to']])

                #   for k in temp_data.iloc[neigh_temp.predict_proba(flower).argsort(axis=1)[:,:-4:-1][0]]['id']:
                    #print('-', df[df['id'] == k]['name'].values[0])
                    #print()
                main_data[main_data['flower_beds']==31]
    except Exception:
        near_flowers = [] 


    # In[ ]:


    #temp_data = temp_data[(temp_data['height_to']>100) & (temp_data['height_to']<170)]
    #temp_data


    # In[ ]:


    df[df['name'].str.contains("Столвик Голд голубой с желтой листвой")]


    # In[ ]:
    return flower_beds_num, near_flowers



