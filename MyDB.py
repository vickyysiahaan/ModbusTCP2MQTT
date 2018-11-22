from time import strftime, localtime
import MySQLdb
import csv
import os, inspect, json

FolderPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

class DataBase(object):
    def __init__(self):
        self.connection = MySQLdb.connect(
                              host = "localhost",
                              #user = "gspe",
                              user = "root",
                              #passwd = "gspe-intercon",
                              passwd = "",
                              db = "Modbus2MQTT")
        
        self.cursor = self.connection.cursor()
    
    def drop(self):
        for i in range(1,11):
            self.cursor.execute("""DROP TABLE Device%d;"""%i)
            
    def clearRecords(self):
        for i in range(1,11):
            self.cursor.execute("""DELETE FROM Device%d;"""%i)

    def create(self):
        #MODULE SPECIFIC DATA TABLE
        for i in range(1,11):
            self.command = """CREATE TABLE Device%d(
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    device_name VARCHAR(50),
    var_name VARCHAR(50),
    num_val FLOAT NULL DEFAULT NULL,
    str_val VARCHAR(256) NULL DEFAULT NULL)
    """%i
            #print(self.command)
            self.cursor.execute(self.command)

        
    def InsertData(self, dev, dev_name, data_dict):
        key = list(data_dict.keys())
        val = list(data_dict.values())
        timestamp = data_dict['Timestamp']
        for i in range(0, len(key)):
            if key[i] != "Timestamp":
                varname = key[i]
                varval = val[i]
                if type(varval) is str:
                    self.command = """INSERT INTO Device%d(timestamp, device_name, var_name, str_val) VALUES('%s','%s','%s','%s')""" %(dev, timestamp, dev_name, varname, varval)
                    #print(self.command)
                    self.cursor.execute(self.command)
                elif type(varval) is int:
                    self.command = """INSERT INTO Device%d(timestamp, device_name, var_name, num_val) VALUES('%s','%s','%s',%d)""" %(dev, timestamp, dev_name, varname, varval)
                    #print(self.command)
                    self.cursor.execute(self.command)
                elif type(varval) is float:
                    self.command = """INSERT INTO Device%d(timestamp, device_name, var_name, num_val) VALUES('%s','%s','%s',%f)""" %(dev, timestamp, dev_name, varname, varval)
                    #print(self.command)
                    self.cursor.execute(self.command)
        
    #Function to commit any changes in local database
    def commit(self):
        self.connection.commit()

    #Function to close connection to local database
    def close(self):
        self.connection.close()


"""
db = DataBase()
#db.create()
#db.drop()
from time import strftime, localtime
data = {"nama": "Vicky", "umur":23, "tinggi":170.578, "Timestamp":strftime("%Y-%m-%d %H:%M:%S", localtime())}
db.InsertData(1, "orang", data)
db.commit()
db.close()
"""

