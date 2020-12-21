import config

table = 'fb_keyword_var'

config_Zhu = 1 #主关键词
config_Var1 = 2 #变量1
config_Var2 = 3 #变量2
config_Var3 = 4 #变量3

keyword_table_1 = 1
keyword_table_2 = 2
keyword_table_3 = 3
keyword_table_4 = 4
keyword_table_5 = 5

def keywordDataVar1(admin_id):
    cursor = config.config_online()
    sql = "SELECT type,keyword FROM {} WHERE admin_id = '%s' and theme = '%s'".format(table)
    data = (admin_id,keyword_table_1)
    cursor.execute(sql % data)
    return cursor.fetchall()

def keywordDataVar2(admin_id):
    cursor = config.config_online()
    sql = "SELECT type,keyword FROM {} WHERE admin_id = '%s' and theme = '%s'".format(table)
    data = (admin_id,keyword_table_2)
    cursor.execute(sql % data)
    return cursor.fetchall()

def keywordDataVar3(admin_id):
    cursor = config.config_online()
    sql = "SELECT type,keyword FROM {} WHERE admin_id = '%s' and theme = '%s'".format(table)
    data = (admin_id,keyword_table_3)
    cursor.execute(sql % data)
    return cursor.fetchall()

def keywordDataVar4(admin_id):
    cursor = config.config_online()
    sql = "SELECT type,keyword FROM {} WHERE admin_id = '%s' and theme = '%s'".format(table)
    data = (admin_id,keyword_table_4)
    cursor.execute(sql % data)
    return cursor.fetchall()

def keywordDataVar5(admin_id):
    cursor = config.config_online()
    sql = "SELECT type,keyword FROM {} WHERE admin_id = '%s' and theme = '%s'".format(table)
    data = (admin_id,keyword_table_5)
    cursor.execute(sql % data)
    return cursor.fetchall()

def deleteAll(admin_id,theme):
    sqlDel = "DELETE FROM {} WHERE admin_id = '%s' and theme = '%s'".format(table)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        data = (admin_id,theme)
        cursor.execute(sqlDel,data)
        commit.commit()
        return cursor.fetchall()
    except Exception as e:
        print(e)
        commit.rollback()

def add_Data(keyword_list,admin_id,type,theme):
    insertAll = ''
    for info in keyword_list:
        if len(info) > 1:
            insertAll += '("{}",{},{},{}),'.format(info,type,admin_id,theme)
    sql = "INSERT INTO {} (`keyword`, `type`, `admin_id`,`theme`) VALUES {}".format(table,insertAll)

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