from pymysql import connect
import os


class Config:
    conn = None
    cs = None

    def __init__(self, host='127.0.0.1', port=3306, database='test', user='root',
                 password=os.getenv('MySQLPW'), charset='utf8'):
        Config.conn = connect(host=host, port=port, database=database,
                              user=user, password=password, charset=charset)
        Config.cs = Config.conn.cursor()


def query(cmd):
    Config.cs.execute(cmd)
    res = Config.cs.fetchall()
    if len(res) == 1:
        res = res[0]
    return res


def commit():
    # 提交之前的操作，如果之前已经之执行过多次的execute，那么就都进行提交
    Config.conn.commit()


class Retrieve:
    def __init__(self, SN):
        self.SN = SN
        self.IP = self.query('IP')
        self.ID = self.query('ID')

    def query(self, field):
        cmd = 'select `%s` from `INFO` where `SN` = %s' % (field, self.SN)
        res = query(cmd)
        if len(res) == 1:
            res = res[0]
        return res




class Update:

    @classmethod
    def updateIP(cls):
        pass
