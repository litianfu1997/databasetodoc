#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version 3.7.1
#生成数据字典
 
import mysql.connector
import importlib
import sys
 
 
def generate(database_name):
    """
    生成数据库字典表
    """
    importlib.reload(sys)
 
    # 使用前修改配置
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        user='root',
        password='root',
        use_pure=True
    )
 
    cursor = conn.cursor()
 
    cursor.execute(
        "SELECT TABLE_NAME, TABLE_COMMENT FROM information_schema.TABLES WHERE table_type='BASE TABLE' AND TABLE_SCHEMA='%s'" % database_name
    )
 
    tables = cursor.fetchall()
 
    markdown_table_header = """\n\n\n### %s (%s) \n| 字段名称 | 数据类型 | 长度 | 主键 | 为空 | 字段说明 |\n|----| ---- | ---- | ---- | ---- | ---- |\n"""
    markdown_table_row = """| %s | %s | %s | %s | %s | %s |"""
 
    f = open(database_name + '.md', 'w')
 
    for table in tables:
 
        cursor.execute(
            "SELECT  COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, if(COLUMN_KEY='PRI','T',''), if(IS_NULLABLE='YES','T',''), COLUMN_COMMENT "
            "FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s'" % (
                database_name, table[0]
            )
        )
 
        tmp_table = cursor.fetchall()
        p = markdown_table_header % (table[0], remove_newline(table[1]))
        for col in tmp_table:
            p += (remove_newline(markdown_table_row % col) + "\n")
        print(p)
        f.writelines(p)
    print("程序结束，程序退出")
    f.close()
    conn.close()
    sys.exit()
    
 
 
def remove_newline(text):
    """
    去除文本中的换行符号
    """
    return text.replace("\r", "").replace("\n", "")
 
#  opendata_security
#  datax_web

 
if __name__ == '__main__':
    generate('opendata_security')