import pymysql
from jsonpath import jsonpath
from jsonpath_ng import parse


def parse_butie_data(data, id):
    """
    处理补贴数据
    :param data:
    :return:
    """
    # 获取 records
    records = data.get("data", {}).get("records", [])

    # 提取 subsidyMoney
    projectName = jsonpath(data, '$..data.records..projectName')
    projectGrade = jsonpath(data, '$..data.records..projectGrade')
    projectTypeEight = jsonpath(data, '$..data.records..projectTypeEight')
    categorys = jsonpath(data, '$..data.records..categorys')
    dataYear = jsonpath(data, '$..data.records..dataYear')
    subsidyMoney = [record.get("subsidyMoney") for record in records]
    topicNames = [record.get("topicName") for record in records]  # 课题
    productNames = [record.get("productName") for record in records]  # 产品
    states = [record.get("state") for record in records]  # 证书
    personnels = [record.get("personnel") for record in records]  # 补贴对象
    lst = []
    if productNames == []:
        print('没有补贴信息')
        return lst

    type_dict = {
        1: '国家级',
        2: '省级',
        3: '市级',
        4: '区级'
    }

    categorys_dict = {
        1: '全选',
        2: '发改部门',
        3: '工信部门',
        4: '科技部门',
        5: '市监部门',
        6: '其他部门',
    }

    lengths = list(map(len, [projectName, projectGrade, projectTypeEight, categorys, dataYear, subsidyMoney , states]))
    for name, grade, typeEight, category, year, money , topicname ,productname , state , prosonnerl  in zip(projectName, projectGrade, projectTypeEight,
                                                             categorys, dataYear, subsidyMoney , topicNames,productNames,states,personnels):

        if category[0] == None:
            cate = '无'
        else:
            cate = "、".join(map(str, [categorys_dict[i] for i in category]))
        # 使用条件表达式拼接字符串
        result = ''
        if topicname is not None:
            result +='课题：' +   str(topicname) + '、'
        if productname is not None:
            result += '产品：' +  str(productname) + '、'
        if state is not None:
            result += '证书状态：' +  str(state) + '、'
        if prosonnerl is not None:
            result += '补贴对象：' +  str(prosonnerl)

        # 去掉最后一个 '、' 符号
        result = result.rstrip('、')
        s = {
            'id': id,
            'projectName': name,  # 项目名称
            'projectGrade': type_dict[grade],  # 级别
            'projectTypeEight': typeEight,  # 项目类型
            'categorys': cate,  # 受理部门
            'dataYear': year,  # 年度
            'subsidyMoney': str(money) + 'w',  # 补贴金额
            'qita': result
        }
        lst.append(s)

    # print(lst)
    return lst


def save_base_data(connection, base_info):
    insert_query = '''
    INSERT INTO company_info (
        company_name, company_id, re_name, company_people, company_status, 
        company_start_time, company_money, company_really_money, company_type, company_code, 
        company_nasui_id, company_gongshang_id, company_ctype, company_nasui_zizhi, company_jinkou_code, 
        company_hangye, company_people_num, company_canbao_people_num, company_dengji, company_manage_date, 
        company_hezhun_date, company_haiguan_code, company_english_name, company_reg_addr, company_manage_range
    ) VALUES (
        %(company_name)s, %(company_id)s, %(re_name)s, %(company_people)s, %(company_status)s, 
        %(company_start_time)s, %(company_money)s, %(company_really_money)s, %(company_type)s, %(company_code)s, 
        %(company_nasui_id)s, %(company_gongshang_id)s, %(company_ctype)s, %(company_nasui_zizhi)s, %(company_jinkou_code)s, 
        %(company_hangye)s, %(company_people_num)s, %(company_canbao_people_num)s, %(company_dengji)s, %(company_manage_date)s, 
        %(company_hezhun_date)s, %(company_haiguan_code)s, %(company_english_name)s, %(company_reg_addr)s, %(company_manage_range)s
    );
    '''

    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_query, base_info)
            connection.commit()  # 提交插入操作
            print('插入成功')
    except pymysql.MySQLError as e:
        print(f"Error: {e.args}, {e.args}")


def save_butie_data(conn, butie_info):
    try:
        if len(butie_info) == 0:
            pass
        else:
            for record in butie_info:
                record['dataYear'] = str(record['dataYear'])
                # 插入数据的SQL语句
                insert_query = '''
                    INSERT INTO subsidy_info (
                        company_id, project_name, project_grade, project_type_eight, categorys, data_year, subsidy_money , qita
                    ) VALUES (
                        %(id)s, %(projectName)s, %(projectGrade)s, %(projectTypeEight)s, %(categorys)s, %(dataYear)s, %(subsidyMoney)s , %(qita)s
                    );
                '''

                with conn.cursor() as cursor:
                    cursor.execute(insert_query, record)
                    conn.commit()  # 提交插入操作
            print('插入数据成功')
    except pymysql.MySQLError as e:
        print(f"插入失败: {e}")