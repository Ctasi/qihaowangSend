import config
import json
table = 'fb_sentence'
table_pag = 'fb_paragraph'
# cursor = config.config_online()

def getDataList(admin_id,task_id,config_id):
    try:
        dataList = []
        cursor = config.config_online()
        sql = "SELECT * FROM {} WHERE admin_id = '%s' and task_id = {} and pag_id=0 and config_id = {} order by id asc".format(table,task_id,config_id)
        data = (admin_id)
        cursor.execute(sql % data)
        for info in cursor:
            dataList.append({'id':info[0],'content':info[1]})
        return dataList
    except Exception as e:
        print(e)

def getDataListDuan(admin_id,task_id,pag_id,config_id):
    try:
        dataList = []
        cursor = config.config_online()
        sql = "SELECT * FROM {} WHERE admin_id = '%s' and task_id = {} and pag_id = {} and config_id = {} order by id asc".format(table,task_id,pag_id,config_id)
        data = (admin_id)
        cursor.execute(sql % data)
        for info in cursor:
            dataList.append({'id':info[0],'content':info[1]})
        return dataList
    except Exception as e:
        print(e)

def deleteAll(admin_id,task_id,config_id):
    try:
        cursor = config.config_online()
        sql = "DELETE FROM {} WHERE admin_id = '{}' and task_id = '{}' and config_id = {} and pag_id = 0".format(table,admin_id,task_id,config_id)
        cursor.execute(sql)
    except Exception as e:
        print(e)

def deleteAllDuan(admin_id,task_id,pag_id,config_id):
    try:
        cursor = config.config_online()
        sql = "DELETE FROM {} WHERE admin_id = '{}' and task_id = '{}' and pag_id = '{}' and config_id = '{}'".format(table,admin_id,task_id,pag_id,config_id)
        cursor.execute(sql)
    except Exception as e:
        print(e)

def add_Data(sentenceList,admin_id,task_id,config_id):
    insertAll = ''
    for info in sentenceList:
        if len(info) > 0:
            insertAll += '("{}",{},{},{}),'.format(info,admin_id,task_id,config_id)
    sql = "INSERT INTO {} (`content`, `admin_id`,`task_id`,`config_id`) VALUES {}".format(table,insertAll)

    print(sql[:-1])
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        cursor.execute(sql[:-1])
        commit.commit()
        return 1
    except Exception as e:
        # print(e)
        commit.rollback()

def add_DataDuan(sentenceList,admin_id,task_id,pag_id,config_id):
    insertAll = ''
    for info in sentenceList:
        if len(info) > 0:
            insertAll += '("{}",{},{},{},{}),'.format(info,admin_id,task_id,pag_id,config_id)
    sql = "INSERT INTO {} (`content`, `admin_id`,`task_id`,`pag_id`,`config_id`) VALUES {}".format(table,insertAll)

    # print(sql[:-1])
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        cursor.execute(sql[:-1])
        commit.commit()
        return 1
    except Exception as e:
        # print(e)
        commit.rollback()

def getDataOne(admin_id,task_id,name,config_id):
    sqlDel = "SELECT * FROM {} WHERE admin_id = {} and task_id = '{}' and `name` = '{}' and `config_id` = '{}'".format(table_pag,admin_id,task_id,name,config_id)
    # print(sqlDel)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        data = []
        config.connect.ping(reconnect=True)
        cursor.execute(sqlDel)
        list = []
        for info in cursor:
            list.append(info)
        if len(list) > 0:
            for info in list:
                data = {"id":info[0],"name":info[1]}
            return data
        else:
            return {"id":0,"name":''}
    except Exception as e:
        print(e)
        return {"id":0,"name":''}
        # return cursor.fetchall()

def addPageInfo(admin_id,name,task_id,config_id):
    cursor = config.config_online()
    sql = "INSERT INTO {} (name, admin_id,task_id,config_id) VALUES ( '{}', '{}','{}','{}')".format(table_pag, name,admin_id,task_id,config_id)
    # print(sql)
    cursor.execute(sql)
    for info in cursor:
        return info[0]


def getPagDataList(admin_id,task_id,config_id):
    try:

        dataList = []
        cursor = config.config_online()
        sql =  "SELECT * FROM {} WHERE admin_id = {} and task_id = {} and config_id = {}".format(table_pag,admin_id,task_id,config_id)
        # print(sql)
        config.connect.ping(reconnect=True)
        cursor.execute(sql)
        for info in cursor:
            dataList.append({'id':info[0],'name':info[1]})
        return dataList
    except Exception as e:
        print(e)


def getPagDataList1(admin_id,task_id,config_id):

  try:
        dataList = []

        sql =  "SELECT * FROM {} WHERE `admin_id` = {} and `task_id` = {} and `config_id` = {}".format(table_pag,admin_id,task_id,config_id)
        # print(sql)
        config.connect.ping(reconnect=True)
        cursor = config.config_online()
        cursor.execute(sql)
        for info in cursor:
            dataList.append({'id':info[0],'name':info[1]})
        cursor.close()
        config.connect.close()
        return dataList
  except Exception as e:
      print(e)
def getPagDataListSend(admin_id,task_id,config_id):
    sql = "SELECT `id`,`name` FROM {} WHERE admin_id = {} and task_id = '{}' and config_id = '{}'".format(table_pag,admin_id,task_id,config_id)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        data = []
        cursor.execute(sql)
        list = []
        for info in cursor:
            list.append(info)
        # print(result)
        if len(list) > 0:
            for info in list:
                data.append({'id':info[0],'name':info[1],'data':[]})
            return data
        else:
            return []
    except Exception as e:
        print(e)
        # return cursor.fetchall()

def getSendSenPag(task_id,config_id,pagList):
    # if len(notWhere) > 0:
    #     notWhere = 'id not in ({}) and'.format(notWhere[:-1])
    sql = "select pag_id,content from {} where  task_id = {} and config_id = {}".format(table, task_id, config_id)
    print(sql)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        # 先删
        # data = ''
        data = []
        cursor.execute(sql)
        i = 0
        for info2 in pagList:
            for info in cursor:
                print(info)
                if info2['id'] == info[0]:
                    pagList[i]['data'].append(info)
            i += 1

        return pagList
    except Exception as e:
        print(12313123)
        print(e)
        return ['error']
        # return cursor.fetchall()

def getSendSen(admin_id,task_id,config_id):
    sql = "select `content` from {} where pag_id = 0 and admin_id = {} and task_id = {} and config_id = {}".format(table,admin_id,task_id,config_id)
#     # print(sql)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        # data = ''
        cursor.execute(sql)
        list = []
        for info in cursor:
            list.append(info[0])
        print(2222222222211111111111)
        print(list)
        if len(list) > 0:
            return list
        else:
            return []
    except Exception as e:
        print(e)
        return '&nbsp;'
        # return cursor.fetchall()
