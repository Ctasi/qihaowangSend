import config
import apiAll
table = 'fb_album'
table_img = 'fb_img'

def addAlbum(admin_id,urlList,type,task_id,config_id):
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        for url in urlList:
            sql_sel = "SELECT * FROM {} WHERE admin_id = {} and task_id = '{}' and url = '{}' and type = '{}' and config_id = '{}'".format(table_img, admin_id,
                                                                                                  task_id, url,type,config_id)
            cursor.execute(sql_sel)
            data = []
            for info in cursor:
                data.append(info[0])
            if len(data) == 0:
                sql = "INSERT INTO {} (url, admin_id, type,task_id,config_id) VALUES ( '{}', '{}','{}','{}','{}')".format(table_img,url, admin_id,type,task_id,config_id)
                # 先删
                cursor.execute(sql)
                result = cursor.fetchall()
        commit.commit()
    except Exception as e:
        print(e)
        commit.rollback()

def addAlbumImg(admin_id,url,task_id,album_id,config_id):
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        url = url.replace(apiAll.website,'')
        # sqlDel = "DELETE FROM {} WHERE admin_id = '{}' and type = '{}' and task_id = '{}'".format(table_img,admin_id,type,task_id)
        # cursor.execute(sqlDel)
        sql = "INSERT INTO {} (url, type, admin_id,album_id,task_id,config_id) VALUES ( '{}', '{}','{}','{}','{}','{}')".format(table_img,url.replace(apiAll.website+'/',''),3, admin_id,album_id,task_id,config_id)
        # 先删
        print(sql)
        cursor.execute(sql)
        commit.commit()
    except Exception as e:
        print(e)
        commit.rollback()

def delAlbumImg(idList):
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        for id in idList:
            sqlDel = "DELETE FROM {} WHERE id = '{}'".format(table_img,id)
            cursor.execute(sqlDel)
    except Exception as e:
        print(e)

def delAlbumImgClear(type,admin_id,task_id,album_id,config_id):
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        sqlDel = "DELETE FROM {} WHERE type = '{}' and admin_id = '{}' and task_id = '{}' and album_id = '{}' and config_id = '{}'".format(table_img,type,admin_id,task_id,album_id,config_id)
        cursor.execute(sqlDel)
    except Exception as e:
        print(e)

def addAlbumAll(admin_id,urlList,album_id,task_id,type,config_id):
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        sqlDel = "DELETE FROM {} WHERE admin_id = '{}' and type = '{}' and task_id = '{}' and album_id = '{}' and config_id = '{}'".format(table_img,admin_id,type,task_id,album_id,config_id)
        # print(sqlDel)
        cursor.execute(sqlDel)
        # print(urlList)
        for url in urlList:
            sql = "INSERT INTO {} (url, admin_id, type,task_id,album_id,config_id) VALUES ( '{}', '{}','{}','{}','{}','{}')".format(table_img,url, admin_id,type,task_id,album_id,config_id)
            # 先删
            cursor.execute(sql)
            result = cursor.fetchall()
        commit.commit()
    except Exception as e:
        print(e)
        commit.rollback()

def getDataList(admin_id,task_id,config_id):
    sql = "SELECT * FROM {} WHERE admin_id = {} and task_id = '{}' and config_id = '{}'".format(table,admin_id,task_id,config_id)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        data = []
        cursor.execute(sql)
        list = []
        for info in cursor:
            list.append(info)
        print(list)
        if len(list) > 0:
            for info in list:
                data.append({"id":info[0],"name":info[1]})
            return data
    except Exception as e:
        print(e)
        # return cursor.fetchall()

def getDataOne(admin_id,task_id,name,config_id):
    sqlDel = "SELECT * FROM {} WHERE admin_id = {} and task_id = '{}' and `name` = '{}' and `config_id` = '{}'".format(table,admin_id,task_id,name,config_id)
#     # print(sqlDel)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        data = []
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
        # return cursor.fetchall()

def addAlbumInfo(admin_id,name,task_id,config_id):
    cursor = config.config_online()
    try:
        sql = "INSERT INTO {} (name, admin_id,task_id,config_id) VALUES ( '{}', '{}','{}','{}')".format(table, name,admin_id,task_id,config_id)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)

def titleImgData(admin_id,task_id,config_id):
    # commit = config.config_Commit()
    try:
        data = []
        cursor = config.config_online()
        sql = "SELECT * FROM {} WHERE admin_id = '{}' and type = '1' and task_id = '{}' and config_id = '{}'".format(table_img, admin_id,task_id,config_id)

        # print(sql)
        cursor.execute(sql)
        for info in cursor:
            data.append({"id": info[0], "url": info[1]})
        return data
    except Exception as e:
        print(e)
        # return cursor.fetchall()

def titleImgDataSend(admin_id,task_id,max_list,config_id):
    try:
        sqlDel = "SELECT * FROM {} WHERE admin_id = {} and type = 1 and task_id = '{}' and config_id = '{}' order by rand() LIMIT {}".format(table_img, admin_id,task_id,config_id,int(max_list)+1)
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
            data.append(info[1])
        return data
    except Exception as e:
        print(e)
        # return cursor.fetchall()

def randomImgData(admin_id,task_id,config_id):
    sqlDel = "SELECT * FROM {} WHERE admin_id = {} and type = 2 and task_id = '{}' and config_id = '{}'".format(table_img, admin_id,task_id,config_id)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        # 先删
        data = []
        cursor.execute(sqlDel)
        for info in cursor:
            data.append({"id": info[0], "url": info[1]})
        return data
    except Exception as e:
        print(e)
        # return cursor.fetchall()

def albumImgData(admin_id,task_id,album_id,config_id):
    sql = "SELECT * FROM {} WHERE admin_id = {} and type = 3 and task_id = '{}' and album_id = {} and config_id = '{}'".format(table_img, admin_id,task_id,album_id,config_id)
    print(sql)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        # 先删
        data = []
        cursor.execute(sql)
        for info in cursor:
            data.append({"id": info[0], "url": info[1]})
        return data
    except Exception as e:
        print(e)
        # return cursor.fetchall()

def getSendImg(admin_id,task_id,type,config_id,notWhere):
    if len(notWhere) > 0:
        notWhere = 'id not in ({}) and'.format(notWhere[:-1])
    sql = "select id,url from {} where {} admin_id = {} and task_id = {} and type={} and config_id ={} order by rand() LIMIT 1".format(table_img,notWhere,admin_id,task_id,type,config_id)
    print(sql)
    cursor = config.config_online()
    commit = config.config_Commit()
    try:
        #先删
        # data = ''
        cursor.execute(sql)
        for info in cursor:
            return info
        else:
            return ['error']
    except Exception as e:
        # print(e)
        return ['error']
        # return cursor.fetchall()