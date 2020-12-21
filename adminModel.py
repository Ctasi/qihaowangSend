import config
import apiAll
table = 'fb_admin'


def getInfo(task_id,config_id):
    sql = "SELECT `username`,`password`,`token` FROM {} WHERE task_id = '{}' and config_id = '{}'".format(table,task_id,config_id)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        data = []
        cursor.execute(sql)

        for info in cursor:
            if info is not None:
                return {"username":info[0],"password":info[1],"token":info[2]}

        print(2222222222)
        return {"username": '', "password": '', "token": ''}
    except Exception as e:
        print('此任务没有配置')
        return {"username": '', "password": '', "token": ''}
        # return cursor.fetchall()

def updateToken(task_id,token,config_id):
    try:
        cursor = config.config_online()
        sql ="UPDATE {} SET token = '{}' WHERE task_id = '{}' and config_id = '{}'".format(table,token,task_id,config_id)
        print(sql)
        cursor.execute(sql)
        for info in cursor:
            print(info)
    except Exception as e:
        print(e)
        return []

def getToken(username,task_id,config_id):
    try:
        cursor = config.config_online()
        sql ="SELECT `token` FROM {} WHERE `username` = '{}' and `task_id` = '{}' and `config_id` = '{}'".format(table,username,task_id,config_id)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print(e)
        return ''

def updateUserInfo(username,password,task_id,token,config_id):
    try:
        cursor = config.config_online()
        sql ="UPDATE {} SET username = '{}',password= '{}',token='{}' WHERE task_id = {} and config_id = {}".format(table,username,password,token,task_id,config_id)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        return []

def addConfig(task_id,config_id):
    print()
    insertAll = '("{}","{}"),'.format(task_id,config_id)
    sql = "INSERT INTO {} ( `task_id`,`config_id`) VALUES {}".format(table, insertAll)
    print(sql)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        cursor.execute(sql[:-1])
        commit.commit()
        return 1
    except Exception as e:
        print(e)
        commit.rollback()