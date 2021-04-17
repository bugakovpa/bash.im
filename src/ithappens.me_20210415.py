'''
Created on 05 мая 2020 г.

@author: kit
1. Создали пустую БД.
2. Начинаем заполнять её.

'''

from bs4 import BeautifulSoup
import sqlite3
import requests
from datetime import datetime
import time

#https://bash.im/quote/460870
#url = "https://bash.im/quote/460870".format(1)
#url = "https://bash.im/quote/460869".format(1)
#url = "https://bash.im/quote/460868".format(1)
# Кривые цитаты, считаем сколько их штук
DebugMode = False ## Выводим или не выводим отладочные сообщения по текту программы.
Trottling = 0 ## Битые цитаты.

conn = sqlite3.connect('bash.im.db.sqlite3')
c = conn.cursor()
c.execute('PRAGMA encoding = "UTF-8"')
## Базу создали ранее
##c.execute("CREATE TABLE IF NOT EXISTS bash(_id_key INTEGER PRIMARY KEY AUTOINCREMENT, id_history INT, title VARCHAR(255), content  TEXT)")
c.execute("begin")

NewRecord = 0  ## Счётчик новых записей. 

for id_history in range (7300, 13494+1): ## На текущий момент существует 13494 цитата.
    # Запрос в БД.
    
    ##SELECT column1, column2....columnN
    ##FROM table_name
    ##WHERE column_name BETWEEN val-1 AND val-2;
        
    #INSERT INTO table_name( column1, column2....columnN) VALUES ( value1, value2....valueN);
    #sql = 'INSERT INTO bash VALUES (?, ?, ?, ?)', (i, author, title, content)
    #sql = '''INSERT INTO bash('id_history', 'title', 'content') VALUES (id_history, title, content)'''
    #
    #RecordKorteg = (id_history, title, content)  ## Закинули строку по полям в кортеж.
    
    ## Сформировали SQL запрос к БД.
    ZaprosSQLSelect = "SELECT \"content\" FROM \"ithappens\" WHERE \"id_history\"=" + str(id_history) + ";"
    ##DebugMode = True 
    ##if DebugMode : print("ZaprosSQLSelect :", ZaprosSQLSelect)
    
    KortegFromDB = ()  ## Принудительная типизация переменной в тип "кортеж", без инициализации оной.
    
    c.execute(ZaprosSQLSelect)  ## Спрашиваем БД, получаем кортеж ответа.
    KortegFromDB = c.fetchone()
    ##if DebugMode : print("KortegFromDB :", KortegFromDB)
    ##if DebugMode : print("KortegFromDB[0] :", KortegFromDB[0])  ## Кортеж, нумерация элементов с 0.
    ##if DebugMode : print("type(KortegFromDB) :", type(KortegFromDB))
    ##content = KortegFromDB[0]
    print(" Обрабатываем историю # ", id_history)
    if KortegFromDB[0] == '-':  ## Если мы считали из базы дефолтное значение '-', то начинаем 
        ## считывать с сайта историю с этим номером, анализируем считанное, если считали хрень,
        ## то перепрыгиваем к следующей записи, иначе обновляем запись в БД.
        ## ========================================================================
        ##start_time = datetime.now()  ## Считали текущее значение времени
        ## PING bash.im (23.105.225.229) 56(84) bytes of data.
        ##url = "https://bash.im/quote/" + str(id_history)  ## Считали страничку с инета.
        url = "https://ithappens.me/story/" + str(id_history)  ## Считали страничку с инета.
        
        ##url = "https://23.105.225.229/quote/" + str(id_history)  ## Считали страничку с инета.
        
        r = requests.get(url)
        html_doc = r.text
        
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        tStr=str(soup)
        # Нашли в "сыром" тексте - само сообщение и вырезали его.
        #tStr = tStr[(tStr.find('<div class="quote__body">')+32):(tStr.find('</div>' ,(tStr.find('<div class="quote__body">') ))-1)]
        tStr = tStr[(tStr.find('<div class="text" itemprop="articleBody">')+45):(tStr.find('</div>' ,(tStr.find('<div class="text" itemprop="articleBody">') ))-5)]
        
        print (tStr)
        ##a = input()
        
        # End of string
        CRLF = str(chr(13) + chr(10))
        #S.replace(шаблон, замена)
        #chr(число)    Код ASCII в символ
        
        # Заменяем в выходном сообщении символ '<br/>', на "окончание строки в виндовс"
        OchichenMessage = tStr.replace('<br/>', CRLF)
        # Заменяем в выходном сообщении символ '&lt;', на '<'
        OchichenMessage = OchichenMessage.replace('&lt;', '<')
        # Заменяем в выходном сообщении символ &gt;', на '>'
        OchichenMessage = OchichenMessage.replace('&gt;', '>')
        
        ## Если в результате анализа, нам выдали вот это, то значит вместо нормальной цитаты мы наткнулись на битую цитату.
        ## Перепрыгиваем к следующей записи и в БД и в интернете, увеличив счётчик "битых" цитат.
        if ((OchichenMessage.find('Утверждено <b>')) > -1):
            Trottling = Trottling + 1  ## Увеличиваем счётчик "битых" цитат.
            print("    Кривых цитат было встречено: ", Trottling, " шт." )
            ## Завершаем итерацию цикла for
            continue
        else:  ## Значит мы нашли нормальную байку, добавляем её в БД.
            NewRecord = NewRecord + 1
            ##if DebugMode : print(OchichenMessage)
            ## Формируем запись в БД 
            ##id_history ##
            ##title = " История номер: " + str(id_history)     
            content = OchichenMessage
            #
            #INSERT INTO table_name( column1, column2....columnN) VALUES ( value1, value2....valueN);
            #sql = 'INSERT INTO bash VALUES (?, ?, ?, ?)', (i, author, title, content)
            ##sql = '''INSERT INTO bash('id_history', 'title', 'content') VALUES (id_history, title, content)'''
            
            ##RecordKorteg = (id_history, title, content)  ## Закинули строку по полям в кортеж.
            ##RecordKorteg = (content)  ## Закинули строку по полям в кортеж.
            ##print ("RecordKorteg:", RecordKorteg)
            ##ZaprosSQLInsert = "INSERT INTO \"bash\" (\"id_history\", \
            ##\"title\", \
            ##\"content\") VALUES (?, ?, ?);" ## 3 fields
            
            ##UPDATE table_name
            ##SET column1 = value1, column2 = value2....columnN=valueN
            ##[ WHERE  CONDITION ];
            ## Убираем апострофы внутри записи, заменяя их пробелами.
            content = content.replace('\'', ' ')
            ZaprosSQLUpdate = "UPDATE \"ithappens\" SET \"content\" = \'" + str(content) + "\' WHERE \"id_history\"=" + str(id_history) + ";"
            ##if DebugMode : print("ZaprosSQLUpdate :", ZaprosSQLUpdate) 
            
            # Вставляем распарсенную запись в БД
            #c.execute(sql)
            #cur.execute(ZaprosSQLInsertADMP, ADMPRecordKorteg)  ## Записываем кортеж в БД.
            c.execute(ZaprosSQLUpdate)  ## Записываем кортеж в БД.
            # Синхронизируем БД
            if (id_history % 100 == 0): ## Записываем каждые 10 000 записей
                    c.execute("commit")  ## Фиксируем записи в БД.
                    print("\n   В БД зафиксировали историю номер ################################################## ", id_history, "\n")
            ##print('На обработку записи было затрачено: ', datetime.now() - start_time)
            ##c.execute("commit")  ## Фиксируем записи в БД.
            ##print("\n   В БД зафиксировали историю номер ############################### ", id_history, "\n")
            # Ждём одну секунду
            time.sleep(1)
        ## ======================================================================== 
    
    ##ZaprosSQLInsert = "INSERT INTO \"bash\" (\"id_history\", \
    ##\"title\", \
    ##\"content\") VALUES (?, ?, ?);" ## 3 fields
    #if DebugMode : print("ZaprosSQLInsert :", ZaprosSQLInsert) 
    
    # Вставляем распарсенную запись в БД
    #c.execute(sql)
    #cur.execute(ZaprosSQLInsertADMP, ADMPRecordKorteg)  ## Записываем кортеж в БД.
    ##c.execute(ZaprosSQLInsert, RecordKorteg)  ## Записываем кортеж в БД.
    
    
    # Ждём одну секунду
    #time.sleep(1)
    ##print('===============================================')
    
c.execute("commit")  ## Фиксируем записи в БД.
print(" Кривых цитат было встречено: ", Trottling, " шт.")
print("\n   Program complete!!!")
