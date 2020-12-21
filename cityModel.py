import config

table = 'fb_city'

Level_Province = 1  #省
Level_City = 2      #市
Level_County = 3    #县


def getProvince():
    sql = "SELECT `name` FROM {} WHERE `level` = '%s' ".format(table)
    data = (Level_Province)
    cursor = config.config_online()
    cursor.execute(sql % data)
    city_list = []
    # print(cursor.fetchall())
    for row in cursor:
        city_list.append(row[0])
    return city_list

def getSelectedDataAll(city,is_pro,is_city,is_xian,is_regionsp):
    city_all = []
    for name in city:
        sql = "SELECT `name`,`id` FROM {} WHERE `name` = '%s' ".format(table)
        data = (name)
        cursor = config.config_online()
        cursor.execute(sql % data)
        for row_p in cursor:
            sql = "SELECT `name`,`id` FROM {} WHERE `parent_id` = '%s' ".format(table)
            data = (row_p[1])
            cursor = config.config_online()
            cursor.execute(sql % data)
            for row_c in cursor:
                sql = "SELECT `name`,`id` FROM {} WHERE `parent_id` = '%s' ".format(table)
                data = (row_c[1])
                cursor = config.config_online()
                cursor.execute(sql % data)
                for row_x in cursor:
                    newname = row_x[0]
                    if len(newname) > 2:
                        if is_xian == 1:
                            if '县' in newname[-1]:
                                newname = newname[:-1]
                        if is_regionsp == 1:
                            newname = newname.replace('自治区', '')
                            newname = newname.replace('自治县', '')
                            newname = newname.replace('自治州', '')
                            newname = newname.replace('自治乡', '')
                            if '区' in newname[-1]:
                                newname = newname[:-1]
                    proname = row_p[0]
                    cityname = row_c[0]
                    if is_pro == 1:
                        if '省' in proname[-1]:
                            proname = proname[:-1]
                    if is_city == 1:
                        if '市' in cityname[-1]:
                            cityname = cityname[:-1]
                    city_all.append(proname+cityname+newname)

    return clearData(city_all,is_pro,is_city,is_xian,is_regionsp)

def getSelectedDataProCity(city,is_pro,is_city,is_xian,is_regionsp):
    city_all = []
    for name in city:
        sql = "SELECT `name`,`id` FROM {} WHERE `name` = '%s' ".format(table)
        data = (name)
        cursor = config.config_online()
        cursor.execute(sql % data)
        # print(cursor.fetchall())
        for row_p in cursor:
            sql = "SELECT `name`,`id` FROM {} WHERE `parent_id` = '%s' ".format(table)
            data = (row_p[1])
            cursor = config.config_online()
            cursor.execute(sql % data)
            for row_c in cursor:
                proname = row_p[0]
                cityname = row_c[0]
                if is_pro == 1:
                    if '省' in proname[-1]:
                        proname = proname[:-1]
                if is_city == 1:
                    if '市' in cityname[-1]:
                        cityname = cityname[:-1]

                city_all.append(proname+cityname)

    return clearData(city_all,is_pro,is_city,is_xian,is_regionsp)

def getSelectedDataProXian(city,is_pro,is_city,is_xian,is_regionsp):
    city_all = []
    for name in city:
        sql = "SELECT `name`,`id` FROM {} WHERE `name` = '%s' ".format(table)
        data = (name)
        cursor = config.config_online()
        cursor.execute(sql % data)
        # print(cursor.fetchall())
        for row_p in cursor:
            sql = "SELECT `name`,`id` FROM {} WHERE `parent_id` = '%s' ".format(table)
            data = (row_p[1])
            cursor = config.config_online()
            cursor.execute(sql % data)
            for row_c in cursor:
                sql = "SELECT `name`,`id` FROM {} WHERE `parent_id` = '%s' ".format(table)
                data = (row_c[1])
                cursor = config.config_online()
                cursor.execute(sql % data)
                for row_x in cursor:
                    try:
                        newname = row_x[0]
                        if len(newname) > 2:
                            if is_xian == 1:
                                if '县' in newname[-1]:
                                    newname=newname[:-1]
                                # newname = newname.replace('县', '')
                            if is_regionsp == 1:
                                newname = newname.replace('自治区', '')
                                newname = newname.replace('自治县', '')
                                newname = newname.replace('自治州', '')
                                newname = newname.replace('自治乡', '')
                                if '区' in newname[-1]:
                                    newname=newname[:-1]
                                # newname = newname.replace('区', '')

                        proname = row_p[0]
                        if is_pro == 1:
                            if '省' in proname[-1]:
                                proname = proname[:-1]

                        city_all.append(proname + newname)

                    except Exception as e:
                        print(e)

    return clearData(city_all,is_pro,is_city,is_xian,is_regionsp)

def getSelectedDataPro(city,is_pro,is_city,is_xian,is_regionsp):
    city_all = []
    for name in city:
        sql = "SELECT `name`,`id` FROM {} WHERE `name` = '%s' ".format(table)
        data = (name)
        cursor = config.config_online()
        cursor.execute(sql % data)
        for row in cursor:
            proname = row[0]
            if is_pro == 1:
                if '省' in proname[-1]:
                    proname = proname[:-1]
            city_all.append(proname)

    return clearData(city_all,is_pro,is_city,is_xian,is_regionsp)

def getSelectedDataCityXian(city,is_pro,is_city,is_xian,is_regionsp):
    city_all = []
    for name in city:
        sql = "SELECT `name`,`id` FROM {} WHERE `name` = '%s' ".format(table)
        data = (name)
        cursor = config.config_online()
        cursor.execute(sql % data)
        for row_p in cursor:
            sql = "SELECT `name`,`id` FROM {} WHERE `parent_id` = '%s' ".format(table)
            data = (row_p[1])
            cursor = config.config_online()
            cursor.execute(sql % data)
            for row_c in cursor:
                sql = "SELECT `name`,`id` FROM {} WHERE `parent_id` = '%s' ".format(table)
                data = (row_c[1])
                cursor = config.config_online()
                cursor.execute(sql % data)
                for row_x in cursor:
                    newname = row_x[0]
                    if len(newname) > 2:
                        if is_xian == 1:
                            if '县' in newname[-1]:
                                newname = newname[:-1]
                            # newname = newname.replace('县', '')
                        if is_regionsp == 1:
                            newname = newname.replace('自治区', '')
                            newname = newname.replace('自治县', '')
                            newname = newname.replace('自治州', '')
                            newname = newname.replace('自治乡', '')
                            newname = newname.replace('区', '')
                    cityname = row_c[0]
                    if is_city == 1:
                        if '市' in cityname:
                            cityname = cityname[:-1]

                    city_all.append(cityname+newname)

    return clearData(city_all,is_pro,is_city,is_xian,is_regionsp)

def getSelectedDataCity(city,is_pro,is_city,is_xian,is_regionsp):
    city_all = []
    for name in city:
        sql = "SELECT `name`,`id` FROM {} WHERE `name` = '%s' ".format(table)
        data = (name)
        cursor = config.config_online()
        cursor.execute(sql % data)
        for row in cursor:
            sql = "SELECT `name`,`id` FROM {} WHERE `parent_id` = '%s' ".format(table)
            data = (row[1])
            cursor = config.config_online()
            cursor.execute(sql % data)
            for row in cursor:
                cityname = row[0]
                if is_city == 1:
                    if '市' in cityname:
                        cityname = cityname[:-1]
                city_all.append(cityname)

    return clearData(city_all,is_pro,is_city,is_xian,is_regionsp)

def getSelectedDataXian(city,is_pro,is_city,is_xian,is_regionsp):
    city_all = []
    for name in city:
        sql = "SELECT `name`,`id` FROM {} WHERE `name` = '%s' ".format(table)
        data = (name)
        cursor = config.config_online()
        cursor.execute(sql % data)
        # print(cursor.fetchall())
        for row in cursor:
            sql = "SELECT `name`,`id` FROM {} WHERE `parent_id` = '%s' ".format(table)
            data = (row[1])
            cursor = config.config_online()
            cursor.execute(sql % data)
            for row in cursor:
                sql = "SELECT `name`,`id` FROM {} WHERE `parent_id` = '%s' ".format(table)
                data = (row[1])
                cursor = config.config_online()
                cursor.execute(sql % data)
                for row in cursor:
                    cityname = row[0]
                    if is_city == 1:
                        if '市' in cityname:
                            cityname = cityname[:-1]
                    city_all.append(cityname)

    return clearData(city_all,is_pro,is_city,is_xian,is_regionsp)

def clearData(city_all,is_pro,is_city,is_xian,is_regionsp):
    city_all_new= []
    for name in city_all:
        city_all_new.append(name)
    return city_all_new

# getProvince()
