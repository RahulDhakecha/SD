import pandas as pd
import pymysql
import os


class AWSMySQLConn:

    def __init__(self, host=os.environ.get("DB_HOST"), port=int(os.environ.get("DB_PORT")),
                 dbname=os.environ.get("DB_NAME"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD")):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
        self.cursor = self.conn.cursor()
        print("Database connection successful")

    def show_tables(self):
        conn = pymysql.connect(self.host, user=self.user, port=self.port, passwd=self.password, db=self.dbname)
        print(pd.read_sql('show tables;', con=conn))
        conn.commit()
        conn.close()

    def execute(self, query):
        conn = pymysql.connect(self.host, user=self.user, port=self.port, passwd=self.password, db=self.dbname)
        cursor = conn.cursor()
        print("Following query executed: {}".format(query))
        cursor.execute(query)
        conn.commit()
        conn.close()

    def execute_query(self, query):
        conn = pymysql.connect(self.host, user=self.user, port=self.port, passwd=self.password, db=self.dbname)
        data = pd.read_sql(query, con=conn)
        # self.cursor.execute(query)
        # rows = self.cursor.fetchall()
        # data = pd.DataFrame(rows)
        conn.commit()
        conn.close()
        return data

    def insert_query(self, table_name, fields, values=[]):
        tuple_values = tuple(values)
        query = "INSERT INTO {} {} VALUES {};".format(table_name, fields, tuple_values)
        print("Following query executed: {}".format(query))
        self.cursor.execute(query)
        self.conn.commit()

    def get_columnnames(self, table_name):
        return pd.read_sql("SELECT column_name from information_schema.columns where "
                           "table_name = '{}';".format(table_name), con=self.conn)

    def get_max_value(self, table_name, column_name):
        query = "SELECT MAX({}) as m FROM {}".format(column_name, table_name)
        return pd.read_sql(query, con=self.conn)['m'].iloc[0]

    def get_unique_values(self, table_name, column_name):
        query = "SELECT {} FROM {} GROUP BY 1;".format(column_name, table_name)
        return list(pd.read_sql(query, con=self.conn).iloc[:, 0])

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    connection = AWSMySQLConn()
    connection.show_tables()
    print(connection.execute_query("select * from RajGroupFollowUpLog where enquiry_key='EN_2020_03_0076'"))
