import config

table = 'fb_username'

def login(username,password):
    sql = "SELECT `username`,`id` FROM {} WHERE `username` = '%s' and `password` = '%s' and type = 1".format(table)
    data = (username,password)
    cursor = config.config_online()
    cursor.execute(sql % data)
    result = cursor.fetchall()
    return result[0]