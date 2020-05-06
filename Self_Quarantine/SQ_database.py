import sqlite3
from sqlite3 import Error
import os

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
def sql_connection(db_path):
    '''
    Establishing connection to database
    '''
    
    try:
            #for creaing a database
            con= sqlite3.connect(db_path, check_same_thread=False)
            print('Connection is established: Database is created in memory')
            return con
    except Error:
            print(Error)

                  
                  

def sql_table(con):
    
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE Processes(P_name text, time_spent integer, strokes integer)")
    con.commit()


def insert_Process(con, P_name, time, strokes):
    
    cursorObj = con.cursor()
    query = "INSERT INTO Processes(P_name, time_spent , strokes )VALUES(?,?,?)"
    cursorObj.execute(query, (P_name, time, strokes))
    con.commit()

                   
                   
def update_Process(con, P_name, strokes):
    
    cursorObj = con.cursor()
    query = "UPDATE Processes SET time_spent = time_spent+1, strokes  = strokes + ? WHERE P_name= ?"
    cursorObj.execute(query, ( strokes, P_name))
    con.commit()

'''                  
                   
if __name__ == "__main__":
     con = sql_connection(DEFAULT_PATH)
     sql_table(con)
                  
'''