import pandas as pd
import pymysql
import os


class AWSMySQLConn:

    def __init__(self, host=os.environ.get("DB_HOST"), port=int(os.environ.get("DB_PORT")),
                 dbname=os.environ.get("DB_NAME"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD")):
        host = host
        port = port
        dbname = dbname
        user = user
        password = password
        self.conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
        self.cursor = self.conn.cursor()
        print("Database connection successful")

    def show_tables(self):
        print(pd.read_sql('show tables;', con=self.conn))
        self.conn.commit()
        self.conn.close()

    def execute_query(self, query):
        return pd.read_sql(query, con=self.conn)

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


if __name__ == '__main__':
    connection = AWSMySQLConn()
    connection.show_tables()
