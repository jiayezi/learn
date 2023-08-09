import pymysql


class DB:
    """
    操作数据库与操作文件类似，在读取修改开始和结束时都需要进行连接（打开），断开（关闭）等固定操作，
    文件读写时可以使用 with （上下文管理器）来简化操作，数据库当然也是可以的
    """
    def __init__(self, host='localhost', port=3306, database='', user='root', passwd='root', charset='utf8'):
        # 建立连接
        self.conn = pymysql.connect(host=host, port=port, database=database, user=user, passwd=passwd, charset=charset)
        # 创建游标
        self.cur = self.conn.cursor()
        # 创建游标，操作设置为字典类型
        # self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        """这个方法的返回值将被赋值给as后面的变量"""
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        """当with后面的代码块全部被执行完之后，将调用前面返回对象的__exit__()方法"""
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()


if __name__ == '__main__':
    with DB(host='120.78.9.140', user='root', passwd='sql', database='myemployees') as db:
        db.execute('select * from employees')
        for row in db:
            print(row)
