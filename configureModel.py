import config
import apiAll
table = 'fb_configure'


def getInfo(task_id):
    sql = "SELECT `id`,`name` FROM {} WHERE task_id = '{}' and status = 1".format(table,task_id)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        data = []
        cursor.execute(sql)
        for info in cursor:
            if info is not None:
                data.append({"id":info[0],"name":info[1]})
        return data
    except Exception as e:
        print('此任务没有配置')
        return []
        # return cursor.fetchall()

def getInfoIdForName(name,task_id):
    sql = "SELECT `id`,`name`,`is_send` FROM {} WHERE task_id = '{}' and name = '{}' and status = 1".format(table,task_id,name)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        data = []
        cursor.execute(sql)
        for info in cursor:
            if info is not None:
                return {"id":info[0],"name":info[1],"is_send":info[2]}
    except Exception as e:
        print('此任务没有配置')
        return []
        # return cursor.fetchall()

def getInfoIdForId(id):
    sql = "SELECT `id`,`name`,`is_send` FROM {} WHERE id = '{}'".format(table,id)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        data = []
        cursor.execute(sql)
        for info in cursor:
            if info is not None:
                return {"id":info[0],"name":info[1],"is_send":info[2]}
    except Exception as e:
        print('此任务没有配置')
        return []
        # return cursor.fetchall()

def getInfoIdForSendList(task_id):
    sql = "SELECT `id`,`name`,`is_send` FROM {} WHERE task_id = '{}'".format(table,task_id)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        data = []
        cursor.execute(sql)
        for info in cursor:
            if info is not None:
                data.append({"id":info[0],"name":info[1],"is_send":info[2]})
        return data
    except Exception as e:
        print('此任务没有配置')
        return []
        # return cursor.fetchall()

def getDataName(name,task_id):
    try:
        cursor = config.config_online()
        sql = 'SELECT id FROM {} WHERE name = "{}" and task_id = "{}" and status = 1'.format(table,name,task_id)
        cursor.execute(sql)
        for info in cursor:
            return info
    except Exception as e:
        # print('没有这个模板')
        return []

def updateStatus(config_id):
    try:
        cursor = config.config_online()
        sql ="UPDATE {} SET status = 0 WHERE id = '{}'".format(table,config_id)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        return []

def updateSend(config_id,send):
    try:
        cursor = config.config_online()
        sql ="UPDATE {} SET is_send = {} WHERE id = '{}'".format(table,send,config_id)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        return []

def addConfig(name,task_id):
    cursor = config.config_online()
    print(33111)
    insertAll = '("{}","{}"),'.format(name, task_id)
    sql2 = "INSERT INTO `{}` (`name`,`task_id`) VALUES {}".format(table,insertAll)
    try:
        print(sql2[:-1])
        cursor.execute(sql2[:-1])
        print(cursor.fetchall())
    except Exception as e:
        print(e)
