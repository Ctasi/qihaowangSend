import config
import json

table = 'fb_send_word'
cursor = config.config_online()

def getDataList(admin_id,task_id,config_id):
    try:
        dataList = []

        sql = "SELECT * FROM {} WHERE admin_id = '%s' and task_id = {} and config_id = {}".format(table,task_id,config_id)
        data = (admin_id)
        cursor.execute(sql % data)
        for info in cursor:
            dataList.append({'id':info[0],'word':info[1],'type':info[4]})
        return dataList
    except Exception as e:
        print(e)

def getDataListSend(admin_id,task_id,config_id):
    try:
        dataList = []

        sql = "SELECT * FROM {} WHERE admin_id = '%s' and task_id = {} and config_id = {}".format(table,task_id,config_id)
        data = (admin_id)
        cursor.execute(sql % data)
        for info in cursor:
            dataList.append(info[1])
        return dataList
    except Exception as e:
        print(e)

def deleteAll(admin_id, task_id,config_id):
    try:
        sql = "DELETE FROM {} WHERE admin_id = '{}' and task_id = '{}' and config_id = '{}'".format(table, admin_id, task_id,config_id)
        cursor.execute(sql)
    except Exception as e:
        print(e)

def add_Data(sentenceList,admin_id,task_id,type,config_id):
    insertAll = ''
    for info in sentenceList:
        if len(info) > 0:
            insertAll += '("{}",{},{},{},{}),'.format(info,admin_id,task_id,type,config_id)
    sql = "INSERT INTO {} (`word`, `admin_id`,`task_id`,`type`,`config_id`) VALUES {}".format(table,insertAll)

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
