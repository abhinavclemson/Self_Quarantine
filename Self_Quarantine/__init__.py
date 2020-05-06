import pymongo
import time
import subprocess
import AppKit
import time
import matplotlib.pyplot as plt
from AppKit import NSWorkspace
from collections import defaultdict
import subprocess
import os
from pynput.keyboard import Listener
from pynput.mouse import Controller
from pynput import keyboard
from threading import Thread
import matplotlib.pyplot as plt
import pandas as pd
from plotly import tools
import plotly.offline as py
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# pl = subprocess.run(['ls', '-la']))
dict = defaultdict(float)
res = []

from pynput import keyboard

pressed = False


# Collect events until released

class main(object):

    def __init__(self):
        self.pos = (0, 0)
        self.con = None
        self.pressed = False

    def on_press(self, key):
        print(f"Key pressed: {key}")
        self.pressed = True

    def __current_active_app(self, con):
        activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']

        mouse = Controller()
        strokes = 0
        my_collection = con

        if strokes == 0:
            with Listener(on_press=self.on_press) as ls:
                def time_out(period_sec: int):
                    time.sleep(period_sec)

                    ls.stop()

                Thread(target=time_out, args=(3,)).start()

                ls.join()
        if self.pressed == True:
            strokes = 3
        else:
            if not mouse.position == self.pos:
                strokes = 3
                self.pos = mouse.position

        self.pressed = False
        exist = my_collection.count_documents({'_id': activeAppName})

        if exist:

            query = {"_id": activeAppName}
            update_query = {'$inc': {"time": 3, "strokes": strokes, }}

            my_collection.update_one(query, update_query)

            print('updated: ' + activeAppName)

        else:
            entry = {'_id': activeAppName, 'time': 3, 'strokes': strokes, 'isProductive': True}
            my_collection.insert_one(entry)

            print('added: ' + activeAppName)

    def __Run(self, con, Time=0):  # returns a dictionary
        # time provide in minutes

        self.con = con
        sec = 0
        total_time = Time

        while sec <= total_time:
            self.__current_active_app(con)
            sec += 3
        self.ChooseProductive(con)
        self.Plot(con)

        return

    def Plot(self, con):
        label_P = []
        label_NP = []

        timeP = []
        timeNP = []

        Hist_P=[]
        Hist_NP=[]


        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        total_time =0
        total_Ptime=0
        total_NPtime=0

        total_active_time=0
        total_active_time_NP=0

        percentageP=[]
        percentageNP=[]

        for obj in con.find():
            if obj['isProductive'] == True:
                label_P.append(obj['_id'])
                timeP.append(obj['time'])
                total_Ptime+= obj['time']

                total_time_spent=obj['time']
                active_time = obj['strokes']

                total_active_time+=obj['strokes']

                percentageP.append((active_time/total_time_spent)*100)
                Hist_P.append(active_time)

            else:
                label_NP.append(obj['_id'])
                timeNP.append(obj['time'])
                total_NPtime+= obj['time']

                total_time_spent=obj['time']
                active_time = obj['strokes']

                total_active_time_NP+=obj['strokes']

                percentageNP.append(active_time/total_time_spent)
                Hist_NP.append(active_time)

            total_time+= obj['time']

        # Create subplots, using 'domain' type for pie charts
        specs = [[{'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}]]
        fig = make_subplots(rows=2, cols=2, specs=specs, subplot_titles=['Total Running time of productive apps: '+str(total_Ptime/60)+' mins',
                                                                         'Total Running time of Non productive apps: '+str(total_NPtime/60)+' mins',
                                                                         'Productivity on Productive apps: '+str(total_active_time/60)+' mins',
                                                                         'Activity on Non-productive apps: ' + str(total_active_time_NP / 60) + ' mins'])


        fig.add_trace(go.Pie(
            values=timeP,
            labels=label_P,
            name = "Productive "
        ), 1,1)
        fig.add_trace(go.Pie(
            values=timeNP,
            labels=label_NP,
            name="Non-Productive ",
        ), 1,2)

        fig.add_trace(go.Pie(
            values=Hist_P,
            labels=label_P,
            name="Productive",
        ),2,1)

        fig.add_trace(go.Pie(
            values=Hist_NP,
            labels=label_NP,
            name="Non-Productive",
        ),2,2)

        fig.update_traces(hoverinfo='label+percent+name')


        fig = go.Figure(fig)
        fig.show()




    def Draw(self, con, minutes=0):
        self.__Run(con, minutes)
        for obj in con.find():
            print(obj['_id'])
            print(obj['time'])
            print(obj['strokes'])
        self.Plot(con)

    def colDrop(self, con):
        con.drop()
        print('Collection dropped')

    def ChooseProductive(self, con):
        print("Choose applications that you think are productive:\n")
        isProductive = input("Enter 'a' for all, otherwise press any key\n")
        for obj in con.find():
            print('app name:', obj['_id'])
            if not isProductive == 'a':

                isProductive = input("Enter 'a' for all, 'y' for yes and 'n' for no: ")
                if isProductive == 'n':
                    query = {"_id": obj['_id']}
                    update_query = {'$set': {'isProductive': False}}
                    con.update_one(query, update_query, upsert=True)
                    print('Not Productive\n')


                elif isProductive == 'y':
                    query = {"_id": obj['_id']}
                    update_query = {'$set': {'isProductive': True}}
                    con.update_one(query, update_query, upsert=True)
                    print('Productive\n')


            elif isProductive == 'a':
                query = {"_id": obj['_id']}
                update_query = {'$set': {'isProductive': True}}
                con.update_one(query, update_query, upsert=True)
                print('Productive\n')



            else:
                isProductive = input("Invalid input, type again: 'a' for all, 'y' for yes and 'n' for no: ")
                print('\n')


if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["ProcessesMongoDB"]
    mycol = mydb["Processes"]

    val = input("PRESS 'y' TO USE EXISTING DATA and 'n' FOR NEW DATA: ")

    if val == 'n':
        main().colDrop(mycol)
        mydb = myclient["ProcessesMongoDB"]
        mycol = mydb["Processes"]

    print("\nDatabase created")
    newval = input("PRESS 'y' TO START A NEW SESSION and 'n' FOR PLOTTING EXISTING DATA: ")
    if newval=="y":
        Time_type = input("PRESS 's' for seconds and 'm' for minutes, 'h' for hours: ")
        Time = float(input("\nEnter time: "))

        if Time_type == 'h':
            Time = Time * 60 * 60
        elif Time_type == 'm':
            Time = Time * 60

        print("Mongo")

        main().Draw(mycol,Time )

        main().ChooseProductive(mycol)

        main().Plot(mycol)

    else:

        main().ChooseProductive(mycol)

        main().Plot(mycol)



