'''
Created on 05 амая. 2020 г.

@author: kit
Создаём полную локальную базу данных.
Пока пустую, просто скелет.
В живую дёргать данные с сайта и втыкать в БД оказалось невозможно:
на разных цитатах программа сваливается в ошибки: нет связи с сайтом и прочее...
Теперь: создаём БД по количеству цитат на сейчас 20200505 это будет 461 061 цитата.
Затем пробуем дергать цитаты с сайта, парсить их и втыкать в бд. (Обновляя записи)
'''


import sqlite3
from datetime import datetime

#https://bash.im/quote/461061 
#url = "https://bash.im/quote/460870".format(1)
#url = "https://bash.im/quote/460869".format(1)
#url = "https://bash.im/quote/460868".format(1)
# Кривые цитаты, считаем сколько их штук
Trottling = 0
DebugMode = False ## Выводим или не выводим отладочные сообщения по текту программы.

conn = sqlite3.connect('habr.im.sqlite3')
c = conn.cursor()
c.execute('PRAGMA encoding = "UTF-8"')
c.execute("CREATE TABLE IF NOT EXISTS bash(_id_key INTEGER PRIMARY KEY AUTOINCREMENT, id_history INT, title VARCHAR(255), content  TEXT)")
c.execute("begin")

for id_history in range (1, 1000000+2):
    start_time = datetime.now()
        
    ##url = "https://bash.im/quote/" + str(id_history)
    ##url="-"
    
    ##r = requests.get(url)
    ##html_doc = r.text
    
    ##soup = BeautifulSoup(html_doc, 'html.parser')
    
    ##tStr=str(soup)
    # Нашли в "сыром" тексте - само сообщение и вырезали его.
    ##tStr = tStr[(tStr.find('<div class="quote__body">')+32):(tStr.find('</div>' ,(tStr.find('<div class="quote__body">') ))-1)]
     
    #print (tStr)
    
    # End of string
    ##CRLF = str(chr(13) + chr(10))
    #S.replace(шаблон, замена)
    #chr(число)    Код ASCII в символ
    
    # Заменяем вы выходном сообщении символ '<br/>', на "окончание строки в виндовс"
    ##OchichenMessage = tStr.replace('<br/>', CRLF)
    # Заменяем вы выходном сообщении символ '&lt;', на '<'
    ##OchichenMessage = OchichenMessage.replace('&lt;', '<')
    # Заменяем вы выходном сообщении символ &gt;', на '>'
    ##OchichenMessage = OchichenMessage.replace('&gt;', '>')
    ##if ((OchichenMessage.find('Утверждено <b>')) > -1):
    ##    Trottling = Trottling + 1
    ##print('OchichenMessage #: ', id_history, "; Кривых цитат было встречено: ", Trottling, " шт.\n" )
    ##print(OchichenMessage)
    ##print()
    ## Формируем запись в БД 
    #id_history ## 655
    title = "История номер: " + str(id_history)     
    ##content = OchichenMessage
    content = "-"
    
    #
    #INSERT INTO table_name( column1, column2....columnN) VALUES ( value1, value2....valueN);
    #sql = 'INSERT INTO bash.im VALUES (?, ?, ?, ?)', (i, author, title, content, tags)
    ##sql = '''INSERT INTO bash('id_history', 'title', 'content') VALUES (id_history, title, content)'''
    
    ##RecordKorteg = (id_history, title, content)  ## Закинули строку по полям в кортеж.
    RecordKorteg = (id_history, title)  ## Закинули строку по полям в кортеж.
    if DebugMode : print ("RecordKorteg:", RecordKorteg)
    
    ##ZaprosSQLInsert = "INSERT INTO \"bash\" (\"id_history\", \
    ##\"title\", \
    ##\"content\") VALUES (?, ?, ?);" ## 3 fields
    ## Correction records: id_history, title
    ZaprosSQLInsert = "UPDATE \"bash\" SET \"id_history\" = '" + str(id_history) + "', \
    \"title\" = '" + title + "' \
    WHERE \"_id_key\" = '" + str(id_history) + "';" ## 2 fields

    if DebugMode : print("ZaprosSQLInsert :", ZaprosSQLInsert) 
    
    # Вставляем распарсенную запись в БД
    #c.execute(sql)
    #cur.execute(ZaprosSQLInsertADMP, ADMPRecordKorteg)  ## Записываем кортеж в БД.
    ##c.execute(ZaprosSQLInsert, RecordKorteg)  ## Записываем кортеж в БД.
    c.execute(ZaprosSQLInsert)  ## Записываем кортеж в БД.
    # Синхронизируем БД
    if (id_history % 10000 == 0): ## Записываем каждые 1 000 записей
            c.execute("commit")
            print('На обработку записи было затрачено: ', datetime.now() - start_time)
    # Ждём одну секунду
    #
    #time.sleep(1)
    if DebugMode : print('===============================================')

c.execute("commit")  ## Записать изменения в БД.
##print(" Кривых цитат было встречено: ", Trottling, " шт.")
print("\n   Program complete!!!")
