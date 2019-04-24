import pandas as pd
import pymysql


class AWSMySQLConn:

    def __init__(self, host="rajgroup.cyjtpl2nvnjr.us-west-2.rds.amazonaws.com", port=3306, dbname="RajGroup", user="raj_2004", password="India123"):
        host = host
        port = port
        dbname = dbname
        user = user
        password = password
        self.conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
        print("Hello1")

    def show_tables(self):
        print("Hello2")
        print(pd.read_sql('show tables;', con=self.conn))

    def execute_query(self, query):
        return pd.read_sql(query, con=self.conn)


if __name__ == '__main__':
    connection = AWSMySQLConn()
    connection.show_tables()
