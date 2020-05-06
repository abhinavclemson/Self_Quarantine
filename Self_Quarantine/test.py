import time
import subprocess
import AppKit
import time
import matplotlib.pyplot as plt
from AppKit import NSWorkspace
from collections import defaultdict
from SQ_database import *
import subprocess
import os
from pynput.mouse import Listener
from pynput.mouse import Controller
from pynput import keyboard
from threading import Thread

#pl = subprocess.run(['ls', '-la']))
dict=defaultdict(float)
res=[]



# Collect events until released

class main(object):
    
    

    def __init__(self):
        self.pos = (0,0)
        self.con=None

    

    def __current_active_app(self, con):
        activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
        strokes=0

        '''
        mouse = Controller()
        stokes=0

        if not mouse.position ==self.pos:
            stokes+=1
            self.pos= mouse.position
            
            
          
        with keyboard.Events() as events:
        # Block at most one second
                try:
                    start_time = time.time()
                    event = events.get(1.0)
                    total_time = (time.time() - start_time)
                    print(total_time)
                    time.sleep(1-total_time)
                    if event:
                        strokes=1
                except:
                        stokes=0
        '''
        cur = con.cursor()
        query='''SELECT P_name FROM Processes WHERE P_name=?'''   
        check = cur.execute(query, (activeAppName,)) 
        print(type(check.fetchone()))
        
        if isinstance((check.fetchone()) , tuple):
            print('updated'+ activeAppName)
            update_Process(con, activeAppName, strokes)

        elif not isinstance((check.fetchone()) , tuple):
            insert_Process(con, activeAppName, 1, strokes)
            print('added'+ activeAppName)


        
        
    def __Run(self,con, minutes=0):#returns a dictionary
        #time provide in minutes

        self.con=con
        sec=0
        total_time= minutes*60
   
        while sec<=total_time:
        
             self.__current_active_app(con)
             sec+=1

          
        con.close()
        return 
    
    def Plot(self, con):
         cur = con.cursor()
         query = '''SELECT P_name FROM Processes'''   
         col = cur.execute(query)
         print(col.fetchall())
         plt.show()
        
    def Draw(self, con, minutes=0):
         self.__Run(con, minutes)

         #self.__Plot(dictionary)
        
        
        
        
        
        


if __name__=="__main__":
    con = sql_connection(DEFAULT_PATH)
    try:
        sql_table(con)
    except:
        pass
    main().Draw(con,1 )
    

