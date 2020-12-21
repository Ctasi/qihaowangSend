import config
import json

table = 'fb_option'


def titleComposeData(admin_id,task_id,field,config_id):
    try:
        cursor = config.config_online()
        sql = "SELECT `option_value` FROM {} WHERE admin_id = '%s' and `option_name` = '{}'and task_id = '{}' and config_id = '{}' LIMIT 1".format(table,field,task_id,config_id)
        # print(sql)
        data = (admin_id)
        cursor.execute(sql % data)
        str = ''
        for info in cursor:
            str = info[0]
        print(str)
        if len(str) > 0:
            return json.loads(str)
        else:
            return []
    except Exception as e:
        print(e)
        return []


def titleComposeSave(admin_id,title,var1,var2,var3,var4,var5,task_id,config_id):
    try:
        title_option = {"title_info": title, 'keyword_var1': var1, 'keyword_var2': var2, 'keyword_var3': var3,
                        'keyword_var4': var4, 'keyword_var5': var5}
        info = titleComposeData(admin_id, task_id, 'title_compose',config_id)
        # print(info)
        if len(info) > 0:
            cursor = config.config_online()
            content = json.dumps(title_option)
            content = content.replace("\\", "\\\\")
            sql = "UPDATE {} SET option_value = '{}' WHERE admin_id = {} and option_name = 'title_compose' and task_id = {} and config_id = {}".format(
                table, content, admin_id, task_id,config_id)
            # print(content)
            cursor.execute(sql)
            result = cursor.fetchall()
        else:
            cursor = config.config_online()
            content = json.dumps(title_option)
            content = content.replace("\\", "\\\\")
            sql = "INSERT INTO {} (option_name, option_value,admin_id,task_id,config_id) VALUES ('title_compose','{}','{}','{}','{}')".format(
                table, content, admin_id, task_id,config_id)
            print(sql)
            cursor.execute(sql)
    except Exception as e:
        print(e)
        return []

def setComposeSave(admin_id,option_value,task_id,config_id):
    try:
        info = titleComposeData(admin_id,task_id,'set_compose',config_id)
        # print(info)
        if len(info) > 0:
            cursor = config.config_online()
            content = json.dumps(option_value)
            content = content.replace("\\", "\\\\")
            sql = "UPDATE {} SET option_value = '{}' WHERE admin_id = {} and option_name = 'set_compose' and task_id = {} and config_id = {}".format(
                table, content, admin_id, task_id,config_id)
            print(content)
            cursor.execute(sql)
        else:
            cursor = config.config_online()
            content = json.dumps(option_value)
            content = content.replace("\\","\\\\")
            sql = "INSERT INTO {} (option_name, option_value,admin_id,task_id,config_id) VALUES ('set_compose','{}','{}','{}','{}')".format(table, content, admin_id, task_id,config_id)
            # print(sql)
            cursor.execute(sql)
    except Exception as e:
        print(e)
        return []

def setSenTypeSave(admin_id,option_value,task_id,config_id):
    try:
        info = titleComposeData(admin_id,task_id,'senType',config_id)
        # print(info)
        if not info is None:
            try:
                if len(info) == 0:
                    cursor = config.config_online()
                    sql = "INSERT INTO {} (option_name, option_value,admin_id,task_id,config_id) VALUES ('senType','{}','{}','{}','{}')".format(
                        table, option_value, admin_id, task_id, config_id)
                    # print(sql)
                    cursor.execute(sql)
                    return
            except Exception as e:
                pass
        cursor = config.config_online()
        sql = "UPDATE {} SET option_value = '{}' WHERE admin_id = {} and option_name = 'senType' and task_id = {} and config_id = {}".format(
            table, option_value, admin_id, task_id,config_id)
        cursor.execute(sql)
    except Exception as e:
        print(e)
        return []

def setDuanTypeSave(admin_id,option_value,task_id,config_id):
    try:
        info = titleComposeData(admin_id,task_id,'duanType',config_id)
        print(info)
        content = json.dumps(option_value)
        content = content.replace("\\", "\\\\")
        if not info is None:
            try:
                if len(info) == 0:
                    cursor = config.config_online()
                    sql = "INSERT INTO {} (option_name, option_value,admin_id,task_id,config_id) VALUES ('duanType','{}','{}','{}','{}')".format(
                        table, content, admin_id, task_id, config_id)
                    print(sql)
                    cursor.execute(sql)
                    return
            except Exception as e:
                pass
            cursor = config.config_online()
            sql = "UPDATE {} SET option_value = '{}' WHERE admin_id = {} and option_name = 'duanType' and task_id = {} and config_id = {}".format(
                table, content, admin_id, task_id,config_id)
            cursor.execute(sql)

    except Exception as e:
        print(e)
        return []

def setTitleSave(admin_id,option_value,task_id,config_id):
    try:
        info = titleComposeData(admin_id,task_id,'title_compose',config_id)
        # print(info)
        if len(info) > 0:
            pass
        else:
            cursor = config.config_online()
            content = json.dumps(option_value)
            content = '{"title_info":"","keyword_var1":"","keyword_var2":"","keyword_var3":"","keyword_var4":"","keyword_var5":""}'
            sql = "INSERT INTO {} (option_name, option_value,admin_id,task_id,config_id) VALUES ('title_compose','{}','{}','{}','{}')".format(table, content, admin_id, task_id,config_id)
            # print(sql)
            cursor.execute(sql)
    except Exception as e:
        print(e)
        return []