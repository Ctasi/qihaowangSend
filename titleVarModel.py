import config
table = 'fb_title_var'

config_Zhu = 1 #主关键词
config_Var1 = 2 #变量1
config_Var2 = 3 #变量2
config_Var3 = 4 #变量3

def titleData(admin_id,task_id,config_id):
    cursor = config.config_online()
    sql = "SELECT type,keyword FROM {} WHERE admin_id = '%s' and task_id = '{}' and config_id = {}".format(table,task_id,config_id)
    data = (admin_id)
    cursor.execute(sql % data)
    data = []
    for info in cursor:
        data.append(info)
    return data

def add_Data(keyword_list,admin_id,type,task_id,config_id):
    insertAll = ''
    for info in keyword_list:
        if len(info) > 0:
            insertAll += '("{}",{},{},{},{}),'.format(info,type,admin_id,task_id,config_id)
    sql = "INSERT INTO {} (`keyword`, `type`, `admin_id`,`task_id`,`config_id`) VALUES {}".format(table,insertAll)

    # print(sql[:-1])
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        cursor.execute(sql[:-1])
        commit.commit()
        return cursor.fetchall()
    except Exception as e:
        # print(e)
        commit.rollback()

def deleteAll(admin_id,task_id,config_id):
    sqlDel = "DELETE FROM {} WHERE admin_id = {} and task_id = {} and config_id = {}".format(table,admin_id,task_id,config_id)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        cursor.execute(sqlDel)
        commit.commit()
        return cursor.fetchall()
    except Exception as e:
        print(e)
        commit.rollback()

def getSendTitleVar(admin_id,task_id,type,config_id):
    sql = "select `keyword` from {} where admin_id = {} and task_id = {} and type={} and config_id = {}".format(table,admin_id,task_id,type,config_id)
#     # print(sql)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        # data = ''
        cursor.execute(sql)
        list = []
        for line in cursor:
            list.append(line[0])
        data = []
        if len(list) > 0:
            for info in list:
                data.append(info[0])
            return data
        else:
            return []
    except Exception as e:
        print(e)
        # return cursor.fetchall()