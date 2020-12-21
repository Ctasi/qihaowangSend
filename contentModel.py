import config
import json

table = 'fb_content'
cursor = config.config_online()

def getDataList(admin_id,task_id,config_id):
    try:
        cursor = config.config_online()
        dataList = []
        sql = "SELECT id,name FROM {} WHERE admin_id = '%s' and task_id = '{}' and config_id = '{}'".format(table,task_id,config_id)
        data = (admin_id)
        cursor.execute(sql % data)
        for info in cursor:
            dataList.append({'id':info[0],'name':info[1],'status':0,'old_name':info[1]})
        return dataList
    except Exception as e:
        print(e)

def getDataContentList(admin_id,task_id,config_id):
    try:
        cursor = config.config_online()
        dataList = []

        sql = "SELECT id,name,content FROM {} WHERE admin_id = '%s' and task_id = '{}' and config_id = '{}'".format(table,task_id,config_id)
        data = (admin_id)
        cursor.execute(sql % data)
        for info in cursor:
            dataList.append(info[2])
        print(dataList)
        return dataList
    except Exception as e:
        print(e)

def getDataContent(id,task_id,config_id):
    try:
        cursor = config.config_online()
        sql = "SELECT content FROM {} WHERE id = '%s' and task_id = '{}' and config_id = '{}'".format(table,task_id,config_id)
        data = (id)
        cursor.execute(sql % data)
        for info in cursor:
            return info[0]
    except Exception as e:
        print(e)

def updateContent(id,content,name,task_id,config_id):
    try:
        cursor = config.config_online()
        sql = "UPDATE {} SET content = '{}',name='{}' WHERE id = {} and task_id = '{}' and config_id = '{}'".format(table,content.replace('"','\\"'),name,id,task_id,config_id)
        # print(sql)
        cursor.execute(sql)
        for info in cursor:
            return info
    except Exception as e:
        print(e)
        return []

def updateName(id,name,task_id,config_id):
    try:
        cursor = config.config_online()
        sql = "UPDATE {} SET name='{}' WHERE id = {} and task_id = '{}' and config_id = '{}'".format(table,name,id,task_id,config_id)
        print(sql)
        cursor.execute(sql)
        for info in cursor:
            return info
    except Exception as e:
        print(e)
        return []

def addOtherContent(name,content,admin_id,task_id,config_id):
    insertAll = '("{}","{}","{}","{}","{}"),'.format(name, content.replace('"','\\"'), admin_id,task_id,config_id)
    sql = "INSERT INTO {} (`name`, `content`, `admin_id`,`task_id`,`config_id`) VALUES {}".format(table, insertAll)
    # print(sql)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        # 先删
        cursor.execute(sql[:-1])
        commit.commit()
        return 1
    except Exception as e:
        print(e)
        commit.rollback()

def getDataName(name,admin_id,task_id,config_id):
    try:
        cursor = config.config_online()
        sql = 'SELECT id FROM {} WHERE name = "{}" and admin_id = {} and task_id = "{}" and config_id = "{}"'.format(table,name,admin_id,task_id,config_id)
        cursor.execute(sql)
        for info in cursor:
            return info
    except Exception as e:
        # print('没有这个模板')
        return []

def getDataNameInfo(name,admin_id,task_id,config_id):
    try:
        cursor = config.config_online()
        sql = 'SELECT * FROM {} WHERE name = "{}" and admin_id = {} and task_id = {} and config_id = {}'.format(table,name,admin_id,task_id,config_id)
        # print(sql)
        cursor.execute(sql)
        for info in cursor:
            return info
    except Exception as e:
        print(e)

def deleteInfo(admin_id,name,task_id,config_id):
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        sqlDel = 'DELETE FROM {} WHERE admin_id = "{}" and name = "{}" and task_id = {} and config_id = {}'.format(table,admin_id,name,task_id,config_id)
        print(sqlDel)
        cursor.execute(sqlDel)
    except Exception as e:
        print(e)