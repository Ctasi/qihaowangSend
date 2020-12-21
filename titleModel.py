import config
import time
table = 'fb_title'

def titleDataAdd(admin_id,titleList,task_id,config_id):
    sqlDel = "DELETE FROM {} WHERE admin_id = {} and task_id = {} and config_id = {}".format(table,admin_id,task_id,config_id)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        # #先删
        # cursor.execute(sqlDel)
        for info in titleList:
            if len(info) > 0:
                sql = 'INSERT INTO {} (title, admin_id,task_id,config_id) VALUES ("{}","{}","{}","{}")'.format(table,info,admin_id,task_id,config_id)
                # data = (info, admin_id,task_id)
                cursor.execute(sql)

        commit.commit()
        return 1
    except Exception as e:
        print(e)
        commit.rollback()
        return 0
        # return cursor.fetchall()

def titleData(admin_id,task_id,status,config_id,page=1,limit=10):
    try:
        sqlDel = "SELECT * FROM {} WHERE admin_id = {} and task_id = '{}' and status = '{}' and config_id = '{}' order by `send_time` desc  LIMIT {},{}".format(table, admin_id,task_id,status,config_id,page,limit)
        print(sqlDel)
        cursor = config.config_online()
    except Exception as e:
        print(e)
    # commit = config.config_Commit()
    try:
        # 先删
        data = []
        # print(sqlDel)
        cursor.execute(sqlDel)
        for info in cursor:
            data.append({"id": info[0], "title": info[1],'status':info[4],'desc':info[5],'send_time':info[6]})
        return data
    except Exception as e:
        print(e)
        # return cursor.fetchall()

def titleDataAll(admin_id,task_id,status,config_id):
    try:
        sqlDel = "SELECT * FROM {} WHERE admin_id = {} and task_id = '{}' and status = '{}' and config_id = '{}' order by `send_time`".format(table, admin_id,task_id,status,config_id)
        print(sqlDel)
        cursor = config.config_online()
    except Exception as e:
        print(e)
    # commit = config.config_Commit()
    try:
        # 先删
        data = []
#         # print(sqlDel)
        cursor.execute(sqlDel)
        for info in cursor:
            data.append({"id": info[0], "title": info[1],'status':info[4],'desc':info[5],'send_time':info[6]})
        return data
    except Exception as e:
        print(e)
        # return cursor.fetchall()

def titleDataCount(admin_id,task_id,status,config_id):
    try:
        sqlDel = "SELECT count(`id`) FROM {} WHERE admin_id = {} and task_id = '{}' and status = '{}' and config_id = '{}'".format(table, admin_id,task_id,status,config_id)
        cursor = config.config_online()
        cursor.execute(sqlDel)
        for info in cursor:
            return info[0]
    except Exception as e:
        print(e)
        # return cursor.fetchall()


def titleDataDai(admin_id,task_id,config_id):
    try:
        sqlDel = "SELECT * FROM {} WHERE admin_id = {} and task_id = '{}' and status = 0 and config_id = {}".format(table, admin_id,task_id,config_id)
        cursor = config.config_online()
    except Exception as e:
        print(e)
    # commit = config.config_Commit()
    try:
        # 先删
        data = []
#         # print(sqlDel)
        cursor.execute(sqlDel)
        for info in cursor:
            data.append({"id": info[0], "title": info[1],'status':info[4]})
        return data
    except Exception as e:
        print(e)
        # return cursor.fetchall()

def titleDataStatus(admin_id,task_id,id,config_id):
    try:
        sqlDel = "SELECT `status` FROM {} WHERE admin_id = {} and task_id = '{}' and id = {} and config_id = {}".format(table, admin_id,task_id,id,config_id)
        cursor = config.config_online()
    except Exception as e:
        print(e)
    # commit = config.config_Commit()
    try:
        # 先删

        cursor.execute(sqlDel)
        for info in cursor:
            return info[0]
    except Exception as e:
        print(e)
        return 2
        # return cursor.fetchall()


def getSendTitle(admin_id,task_id,config_id):
    sql = "select `title` from {} where admin_id = {} and task_id = {} and config_id= {}".format(table,admin_id,task_id,config_id)
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
        # print(result)
        data = []
        if len(list) > 0:
            for info in list:
                data.append(info[0])
        return data
    except Exception as e:
        print(e)
        # return cursor.fetchall()

def updateStatus(admin_id,task_id,status,id,config_id,desc=''):
    try:
        timearray = int(time.time())
        cursor = config.config_online()
        sql ="UPDATE {} SET `status` = '{}',`desc`='{}',`send_time`='{}' WHERE admin_id = {} and task_id = '{}' and id = '{}' and config_id = '{}'".format(table,status,desc,timearray,admin_id,task_id,id,config_id)
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        return []


def deleteOne(admin_id,task_id,id,config_id):
    try:
        cursor = config.config_online()
        sql ="DELETE FROM {} WHERE admin_id = {} and task_id = {} and id = {} and config_id = {}".format(table,admin_id,task_id,id,config_id)
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        return []

def deleteList(admin_id,task_id,status,config_id):
    try:
        cursor = config.config_online()
        sql ="DELETE FROM {} WHERE admin_id = {} and task_id = {} and status = {} and config_id = {}".format(table,admin_id,task_id,status,config_id)
        # print(sql)
        cursor.execute(sql)
    except Exception as e:
        print(e)
        return []
