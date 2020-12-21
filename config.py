import pymysql.cursors
# 连接数据库


# host = '127.0.0.1'
# port = 3306
# user = 'user'
# passwd = ''
# db = 'xxfb'
# charset = 'utf8'
host='123.133.86.57'
port=33089
user='xxfb_qh'
passwd='%mpNUv7s3kWK'
db='xxfb_qh'
charset='utf8'
connect = pymysql.Connect(
    host='123.133.86.57',
    port = 33089,
    user = 'xxfb_qh',
    passwd = '%mpNUv7s3kWK',
    db = 'xxfb_qh',
    charset = 'utf8',
    # host = '127.0.0.1',
    # port = 3306,
    # user = 'user',
    # passwd = '',
    # db = 'xxfb',
    # charset = 'utf8',
)


def config_online():
    # 获取游标
    connect = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, db=db,
                              charset=charset)
    cursor = connect.cursor()
    return cursor

def config_Commit():
    connect = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, db=db,
                              charset=charset)
    # 获取游标
    return connect
