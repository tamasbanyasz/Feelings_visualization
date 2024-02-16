import sqlite3
from sqlite3 import Error


class DatabaseUnity:
    def __init__(self):
        pass

    @classmethod
    def create_connection(cls, db_file):
     
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version) 
        
            return conn
        except Error as e:
            print(e)   
    
        return conn    
    
    @classmethod
    def create_table(cls, conn, create_sql_table):
    
        try:
            c = conn. cursor()
            c.execute(create_sql_table)
    
        except Error as e:
            print(e) 
    
    @classmethod
    def insert_to_table(cls, conn, insert, value):
    
        cur = conn.cursor()
        cur.execute(insert, value)
        conn.commit()
    
        return cur.lastrowid
    
    @classmethod
    def select_all_data(cls, conn, select_all_data):
    
        cur = conn.cursor()
        cur.execute(select_all_data)
    
        rows = cur. fetchall()
    
        for row in rows:
            print(row)

    @classmethod   
    def inner_join_query(cls, conn):
    
        cur = conn. cursor()
        cur.execute('''
                
                    SELECT feelings.id, 
                            another.feelingid, 
                            feelings.feeling, 
                            feelings.first_moment, 
                            another.moments, 
                            another.feeling_value
                         
                    FROM feelings 
                    INNER JOIN another 
                    ON feelings.id = another.feelingid;
                
                    ''')
    
        rows = cur. fetchall()
    
        for row in rows:
            print(row)


if __name__ == "__main__":
    DatabaseUnity()
    
    