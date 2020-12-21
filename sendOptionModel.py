import config
import sentenceModel
import json

table = 'fb_send_option'

def getOption(admin_id,task_id,config_id):
    try:
        cursor = config.config_online()
        sql = "SELECT * FROM {} WHERE admin_id = '%s' and task_id = '{}' and config_id = '{}' LIMIT 1".format(table,task_id,config_id)
        print(sql)
        data = (admin_id)
        cursor.execute(sql % data)
        for info in cursor:
            return info
    except Exception as e:
        print(e)
        return []

def setOption(admin_id,task_id,config_id,info):
    try:
        sendinfo = getOption(admin_id,task_id,config_id)
        print(222222222222)
        print(sendinfo)
        print(3333333333)
        if sendinfo is not None:
            cursor = config.config_online()
            sql = "UPDATE {} SET hour = '{}',minute = '{}',status= '{}',send_hour='{}',send_min='{}',count_num='{}' WHERE task_id = {} and config_id = {}".format(
                table, info['hour'], info['minute'], info['status'], info['send_hour'], info['send_min'], info['count_num'], task_id,config_id)
            print(sql)
            cursor.execute(sql)
        else:
            cursor = config.config_online()
            sql = "INSERT INTO {} (task_id, admin_id,hour,minute,status,config_id,send_hour,send_min,count_num) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(table, task_id, admin_id,info['hour'],info['minute'],info['status'],config_id,info['send_hour'],info['send_min'],info['count_num'])
            print(sql)
            cursor.execute(sql)
    except Exception as e:
        print(e)
        return []

def setOptionStatus(task_id,config_id,status):
    try:
        cursor = config.config_online()
        sql = "UPDATE {} SET status= '{}' WHERE task_id = {} and config_id = {}".format(table,status, task_id,config_id)
        print(sql)
        cursor.execute(sql)
    except Exception as e:
        print(e)
        return []