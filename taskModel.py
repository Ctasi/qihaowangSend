import config
import adminModel
import sentenceModel

table = 'fb_task'

def getListTask(admin_id,page=0,limit=6,search=''):
    sql = "SELECT * FROM {} WHERE `admin_id` =  '{}' and status = 1 and `name` like '%{}%' LIMIT {},{}".format(table,admin_id,search,page,limit)
    # print(sql)
    cursor = config.config_online()
    cursor.execute(sql)
    dataList = []
    for info in cursor:
        print(info)
        dataList.append({'id':str(info[0]),'name':str(info[1]),'speed':str(info[2]),'type':str(info[3]),'admin_id':str(info[5]),'username':str(info[6]),'password':str(info[7]),'token':str(str(info[8])),'config_id':str(info[11]),'shop_id':str(info[12])})
    return dataList

def getListTaskCount(admin_id,search=''):
    sql = "SELECT count(`id`) FROM {} WHERE `admin_id` =  '{}' and status = 1 and `name` like '%{}%'".format(table,admin_id,search)
    # print(sql)
    cursor = config.config_online()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0][0]

def delUserInfo(task_id):
    try:
        cursor = config.config_online()
        sql ="UPDATE {} SET status = 0 WHERE id = {}".format(table,task_id)
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        return []

def updateSpeed(task_id,speed):
    try:
        cursor = config.config_online()
        sql ="UPDATE {} SET speed = '{}' WHERE id = '{}'".format(table,speed,task_id)
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        return ''

def updateStart(admin_id,username,is_start):
    try:
        cursor = config.config_online()
        sql ="UPDATE {} SET is_start = '{}' WHERE admin_id = {} and username = '{}'".format(table,is_start,admin_id,username)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        return ''

def updateConfig(task_id,config_id):
    try:
        cursor = config.config_online()
        sql ="UPDATE {} SET config_id = '{}' WHERE id = '{}'".format(table,config_id,task_id)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        return ''

def getTaskId(admin_id,username):
    try:
        cursor = config.config_online()
        sql ="SELECT `id` FROM {} WHERE `admin_id` =  '{}' and `name` = '{}'".format(table,admin_id,username)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print(e)
        return ''

def addTask(name,type,admin_id):
    # print(sql)
    commit = config.config_Commit()
    cursor = commit.cursor()
    try:
        insertAll = '("{}","{}","{}"),'.format(name, type, admin_id)
        sql = "INSERT INTO {} (`name`, `type`, `admin_id`) VALUES {}".format(table, insertAll)
        print(sql[:-1])
        cursor.execute(sql[:-1])
        # id = getTaskId(admin_id,name)
        # adminModel.addConfig(id,config_id)
        commit.commit()
        return 1
    except Exception as e:
        print(e)
        commit.rollback()

def getTask(admin_id,username):
    try:
        cursor = config.config_online()
        sql ="SELECT `name` FROM {} WHERE `admin_id` =  '{}' and `name` = '{}' and `status` = 1".format(table,admin_id,username)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print(e)
        return ''


def getTaskOne(task_id):
    try:
        cursor = config.config_online()
        sql ="SELECT * FROM {} WHERE `id` =  '{}'".format(table,task_id)
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        info = result[0]
        info = {'task_id':str(info[0]),'name':str(info[1]),'speed':str(info[2]),'type':str(info[3]),'admin_id':str(info[5]),'username':str(info[6]),'password':str(info[7]),'token':str(info[8]),'config_id':str(info[11]),'shop_id':str(info[12])}
        return info
    except Exception as e:
        print(e)
        return ''

def getTaskInfo(admin_id,name):
    try:
        cursor = config.config_online()
        sql ="SELECT * FROM {} WHERE `admin_id` =  '{}' and `name` = '{}' and status = 1".format(table,admin_id,name)
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        info = {'id':result[0][0],'name':result[0][1],'speed':result[0][2],'type':result[0][3],'website':result[0][4],'admin_id':result[0][5],'username':str(result[0][6]),'password':str(result[0][7]),'is_start':result[0][9],'shop_id':result[0][12],'token':str(result[0][8]),'config_id':str(result[0][11])}
        return info
    except Exception as e:
        print(e)
        return []

def updateToken(task_id, token):
    try:
        cursor = config.config_online()
        sql = "UPDATE {} SET token = '{}' WHERE id = '{}'".format(table, token, task_id)
        print(sql)
        cursor.execute(sql)
        for info in cursor:
            print(info)
    except Exception as e:
        print(e)
        return []

def getToken(username,task_id):
    try:
        cursor = config.config_online()
        sql ="SELECT `shop_id` FROM {} WHERE `username` = '{}' and `id` = '{}'".format(table,username,task_id)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print(e)
        return ''

def updateUserInfo(username,password,task_id,shop_id,token):
    try:
        cursor = config.config_online()
        sql ="UPDATE {} SET username = '{}',password= '{}',token='{}',shop_id='{}' WHERE id = {}".format(table,username,password,token,shop_id,task_id)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        return []