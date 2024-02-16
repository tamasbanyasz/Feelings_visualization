from Feelings_package import DatabaseUnity as du
from Feelings_package import Feelings
import plotly.express as px
from pandas import concat
from time import time


create_feelings_table = """
                CREATE TABLE IF NOT EXISTS feelings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feeling TEXT NOT NULL,
                    first_moment REAL,
                    second_moment REAL,
                    third_moment REAL
                    
                );
            """ 
            
insert_to_feelings_table = """
                INSERT INTO feelings(feeling, first_moment, second_moment, third_moment)
                VALUES (?, ?, ?, ?);
    
            """   
select_all_data_from_feelings_table = 'SELECT * FROM feelings;'
             
create_another_table = """
        CREATE TABLE IF NOT EXISTS another (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feelingid INTEGER,
                    moments TEXT,
                    feeling_value REAL,
                    FOREIGN KEY(feelingid) REFERENCES feelings(id)
                    
                );
            """
insert_to_another_table = """
                INSERT INTO another(feelingid, moments, feeling_value)
                VALUES (?, ?, ?);
    
            """
select_all_data_from_another_table = 'SELECT * FROM another;'

conn = du.create_connection(r"Datas_of_feelings_v1_1\\Feelings_package\\feeling.db")
 
if conn is not None:
    du.create_table(conn, create_feelings_table)
    du.create_table(conn, create_another_table)

else:
    print("Error!")
 
start = time()

obj = Feelings()

obj.append_datas_to_starter_dataframe()

# set the df start index from '1'
obj.starter_df.index += len(conn.cursor().execute('SELECT * FROM feelings;').fetchall()) + 1

print("\nStarter df:")
print(obj.starter_df)
print("--------------------------------------------------------")

print("Reshaped df in ascending order: ")
print(obj.reshape_df_columns_by_feelings_and_they_values())
print("--------------------------------------------------------")

# Data visualization
#fig = px.scatter_3d(obj.starter_df, x='First moment', y='Second moment', z='Third moment',
#                    color='Feeling', symbol='Feeling')
#fig.show()

# insert into feelings table
for row in obj.starter_df.itertuples(index=False):
    du.insert_to_table(conn, insert_to_feelings_table, (row[0], row[1], row[2], row[3]))
    
print("\nSelect all data from 'feelings table:")    
du.select_all_data(conn, select_all_data_from_feelings_table)
print("------------------------------------------------")

print("\nFeelings dataframes in list: ")
print(obj.feelings_one_by_one())
print("------------------------------------------------")

# assemble columns with valuues to other sql table
w = concat(obj.feelings_one_by_one(), axis=0).T.drop_duplicates().T.drop_duplicates().reset_index(drop=True)
print("\nReady to insert to 'another' table:")
print(w)
print("------------------------------------------------")

# insert to 'another' table
for row in w.itertuples(index=False):
    du.insert_to_table(conn, insert_to_another_table, (row[1], row[0], row[2]))

print("\nSelect all data from 'another' table:")
du.select_all_data(conn, select_all_data_from_another_table)
print("------------------------------------------------")

print("\nInner join query:")
du.inner_join_query(conn)
end = time()

print("\nTime:")
print(end-start)

