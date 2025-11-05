"""
@ coding : utf-8 
@Time    : 2025/11/4 11:15
@Author  : admin1
@Project : api_auto
@File    : db.py
@Desc    :
@Notes   : 
"""
import pymysql
import yaml

with open("config/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)['db']

class DB:
    def __init__(self):
        self.conn = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config['charset'],
            autocommit=True,
        )
        self.cursor = self.conn.cursor()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def exec(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
    def close(self):
        self.cursor.close()
        self.conn.close()
db = DB()

if __name__ == "__main__":
    ret = db.query("select * from users")
    print(ret)